#!/usr/bin/env python3
"""JSONL trace logger for agent runs (standard library only). Specification: traces/TRACE_SPEC.md.

Records live in traces/stage<N>.jsonl, one JSON object per line. Every read-modify-write is
serialised through the lock file traces/.lock (fcntl.flock) and every rewrite goes through a
temporary file in the same directory followed by os.replace, so concurrent start/end calls from
many processes never lose a record or tear a line. A caller may also wrap the command in
`flock traces/.lock ...`; the inherited lock is detected and reused, not re-taken.

Usage (all paths are relative to the current working directory unless absolute):
  trace_logger.py start --stage 1 --gate G1 --role extraction --instance A --skill skills/extraction \
      --prompt traces/prompts/p.md --model "<model string>" --inputs a.pdf b.pdf \
      [--parent <trace_id>] [--run N] [--settings S] [--started-at ISO] [--ended-at ISO] [--retroactive]
  trace_logger.py end --trace-id <id> --outputs out.csv --selection single_run --human none \
      [--tool-calls '{"total": 12, "by_tool": {"read": 9, "shell": 3}}'] [--safety-stop --safety-stop-subject "<what>"] \
      [--transcript PATH --transcript-kind platform_export|final_report_only] \
      [--tokens-in N --tokens-out N --cost X] [--discarded "<reason>"] [--notes "<text>"] \
      [--started-at ISO] [--ended-at ISO] [--retroactive]
  trace_logger.py check --stage 1            # lists records with no ended_at; exit 0

Exit codes: 0 success; 2 usage or validation error (plain one-line message on stderr, nothing written).
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK_PATH = os.path.join(HERE, ".lock")
TRANSCRIPT_DIR = os.path.join(HERE, "transcripts")
SELECTION_RE = re.compile(r"^(single_run|first_completed|best_of_n:\S+)$")
TRACE_ID_RE = re.compile(r"^s(\d+)-")
TRANSCRIPT_KINDS = ("platform_export", "final_report_only", "none")
ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"


def fail(msg, code=2):
    sys.stderr.write(f"trace_logger: {msg}\n")
    sys.exit(code)


def now():
    return datetime.now(timezone.utc).strftime(ISO_FMT)


def parse_iso(value, flag):
    """Accept ISO 8601 with Z or an offset; return UTC in the record format."""
    v = value.strip()
    try:
        dt = datetime.fromisoformat(v[:-1] + "+00:00" if v.endswith("Z") else v)
    except ValueError:
        fail(f"{flag} must be ISO 8601 (e.g. 2026-10-04T03:34:00Z), got {value!r}")
    if dt.tzinfo is None:
        fail(f"{flag} needs a timezone (use Z for UTC), got {value!r}")
    return dt.astimezone(timezone.utc).strftime(ISO_FMT)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require_files(paths, what):
    for p in paths:
        if not os.path.isfile(p):
            fail(f"{what} path not found: {p}")


def git_short(path):
    if not os.path.exists(path):
        sys.stderr.write(f"trace_logger: skill path {path} does not exist; skill_version recorded as not_recorded\n")
        return "not_recorded"
    try:
        out = subprocess.check_output(["git", "log", "-1", "--format=%h", "--", path],
                                      text=True, stderr=subprocess.DEVNULL).strip()
        return out or "untracked"
    except Exception:
        return "no_git"


def trace_path(stage):
    return os.path.join(HERE, f"stage{stage}.jsonl")


def stage_from_trace_id(tid):
    m = TRACE_ID_RE.match(tid)
    if not m:
        fail(f"malformed trace id {tid!r}: expected prefix s<N>- (e.g. s1-extraction-A-20261004T120000Z-ab12)")
    return m.group(1)


# ---------------------------------------------------------------- locking

def _inherited_lock_fd():
    """Return an inherited file descriptor already open on the lock file (e.g. from `flock traces/.lock cmd`)."""
    try:
        target = os.stat(LOCK_PATH)
    except FileNotFoundError:
        return None
    try:
        fds = [int(x) for x in os.listdir("/proc/self/fd")]
    except OSError:
        fds = range(3, 256)
    for fd in fds:
        try:
            st = os.fstat(fd)
        except OSError:
            continue
        if (st.st_ino, st.st_dev) == (target.st_ino, target.st_dev):
            return fd
    return None


class Locked:
    """Exclusive flock on traces/.lock for the duration of a with-block.

    If the process was launched under `flock traces/.lock ...` the wrapper's descriptor is inherited and
    already holds the lock; flock on that same descriptor succeeds immediately (lock conversion) instead
    of deadlocking against ourselves. Otherwise a fresh descriptor is opened and locked (blocking).
    """

    def __enter__(self):
        os.makedirs(HERE, exist_ok=True)
        self.inherited = _inherited_lock_fd()
        if self.inherited is not None:
            fcntl.flock(self.inherited, fcntl.LOCK_EX)
            self.fd = None
        else:
            self.fd = os.open(LOCK_PATH, os.O_RDWR | os.O_CREAT, 0o644)
            fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            os.close(self.fd)
        # an inherited lock belongs to the wrapper; it is released when the wrapper exits
        return False


# ---------------------------------------------------------------- file I/O

def read_records(path):
    if not os.path.exists(path):
        return []
    recs = []
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError:
                fail(f"{path} line {n} is not valid JSON (torn or hand-edited line); repair it before continuing")
    return recs


def append_record(path, rec):
    data = json.dumps(rec) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def rewrite_records(path, recs):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(prefix=".stage-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
            f.flush()
            os.fsync(f.fileno())
        try:  # keep the stage file's mode (mkstemp creates 0600)
            os.chmod(tmp, os.stat(path).st_mode & 0o777)
        except FileNotFoundError:
            os.chmod(tmp, 0o644)
        os.replace(tmp, path)
        try:
            dfd = os.open(d, os.O_RDONLY)
            os.fsync(dfd)
            os.close(dfd)
        except OSError:
            pass
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ---------------------------------------------------------------- subcommands

def cmd_start(a):
    if not re.fullmatch(r"\d+", str(a.stage)):
        fail(f"--stage must be an integer, got {a.stage!r}")
    require_files([a.prompt], "prompt")
    require_files(a.inputs, "input")
    started = parse_iso(a.started_at, "--started-at") if a.started_at else now()
    ended = parse_iso(a.ended_at, "--ended-at") if a.ended_at else ""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tid = f"s{a.stage}-{a.role}-{a.instance}-{stamp}-{secrets.token_hex(2)}"
    rec = {
        "trace_id": tid, "parent_trace_id": a.parent or "", "stage": str(a.stage), "gate": a.gate,
        "agent_role": a.role, "agent_instance": a.instance,
        "skill_name": os.path.basename(a.skill.rstrip("/")), "skill_version": git_short(a.skill),
        "prompt_ref": a.prompt, "prompt_sha256": sha(a.prompt),
        "model": a.model, "model_settings": a.settings,
        "started_at": started, "ended_at": ended,
        "input_refs": [{"path": p, "sha256": sha(p)} for p in a.inputs], "output_refs": [],
        "tool_calls": {}, "tokens_in": "", "tokens_out": "", "cost_usd": "",
        "run_number": a.run, "selection_policy": "", "discarded_reason": "",
        "human_intervention": "", "safety_stop": False, "safety_stop_subject": "",
        "transcript_ref": "", "transcript_sha256": "", "transcript_kind": "",
        "retroactive": bool(a.retroactive), "notes": "",
    }
    path = trace_path(a.stage)
    with Locked():
        append_record(path, rec)
    print(tid)


def cmd_end(a):
    stage = stage_from_trace_id(a.trace_id)
    path = trace_path(stage)
    if not SELECTION_RE.match(a.selection):
        fail(f"--selection must be single_run, first_completed or best_of_n:<criterion>, got {a.selection!r}")
    require_files(a.outputs, "output")
    if a.transcript is not None:
        require_files([a.transcript], "transcript")
        if a.transcript_kind in (None, "none"):
            fail("--transcript needs --transcript-kind platform_export or final_report_only")
    transcript_kind = a.transcript_kind or "none"
    if a.transcript is None and transcript_kind != "none":
        fail(f"--transcript-kind {transcript_kind} requires --transcript PATH")
    try:
        tool_calls = json.loads(a.tool_calls)
    except json.JSONDecodeError as e:
        fail(f"--tool-calls is not valid JSON ({e.msg}); example: '{{\"total\": 12, \"by_tool\": {{\"read\": 9}}}}'")
    if not isinstance(tool_calls, dict):
        fail("--tool-calls must be a JSON object, e.g. '{\"total\": \"not_exposed\"}'")
    safety_subject = a.safety_stop_subject or ""
    if a.safety_stop and not safety_subject:
        sys.stderr.write("trace_logger: --safety-stop given without --safety-stop-subject; subject recorded as not_recorded\n")
        safety_subject = "not_recorded"
    if safety_subject and not a.safety_stop:
        fail("--safety-stop-subject requires --safety-stop")
    started_override = parse_iso(a.started_at, "--started-at") if a.started_at else None
    ended = parse_iso(a.ended_at, "--ended-at") if a.ended_at else now()
    if not os.path.exists(path):
        fail(f"trace file {path} does not exist; no record for {a.trace_id}")

    with Locked():
        recs = read_records(path)
        hits = [i for i, r in enumerate(recs) if r.get("trace_id") == a.trace_id]
        if not hits:
            fail(f"trace {a.trace_id} not found in {path}")
        r = recs[hits[0]]
        if r.get("ended_at"):
            sys.stderr.write(f"trace_logger: {a.trace_id} already has ended_at {r['ended_at']}; end fields overwritten\n")
        transcript_ref, transcript_sha = "", ""
        if a.transcript is not None:
            os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
            ext = os.path.splitext(a.transcript)[1] or ".txt"
            dest = os.path.join(TRANSCRIPT_DIR, f"{a.trace_id}{ext}")
            shutil.copyfile(a.transcript, dest)
            transcript_ref = os.path.relpath(dest, os.path.dirname(HERE))
            transcript_sha = sha(dest)
        r.update({
            "ended_at": ended,
            "output_refs": [{"path": p, "sha256": sha(p)} for p in a.outputs],
            "tool_calls": tool_calls,
            "tokens_in": a.tokens_in or "not_exposed", "tokens_out": a.tokens_out or "not_exposed",
            "cost_usd": a.cost or "not_exposed",
            "selection_policy": a.selection, "discarded_reason": a.discarded or "",
            "human_intervention": a.human,
            "safety_stop": bool(a.safety_stop), "safety_stop_subject": safety_subject,
            "transcript_ref": transcript_ref, "transcript_sha256": transcript_sha, "transcript_kind": transcript_kind,
            "retroactive": bool(a.retroactive) or bool(r.get("retroactive", False)),
            "notes": a.notes or "",
        })
        if started_override:
            r["started_at"] = started_override
        rewrite_records(path, recs)
    print("completed", a.trace_id)


def cmd_check(a):
    if not re.fullmatch(r"\d+", str(a.stage)):
        fail(f"--stage must be an integer, got {a.stage!r}")
    path = trace_path(a.stage)
    if not os.path.exists(path):
        print(f"no trace file for stage {a.stage} ({path})")
        return
    with Locked():
        recs = read_records(path)
    incomplete = [r for r in recs if not r.get("ended_at")]
    print(f"stage {a.stage}: {len(recs)} records, {len(incomplete)} incomplete (no ended_at)")
    for r in incomplete:
        print(f"  {r.get('trace_id')}  role={r.get('agent_role')} instance={r.get('agent_instance')} started_at={r.get('started_at')}")


# ---------------------------------------------------------------- CLI

def build_parser():
    p = argparse.ArgumentParser(prog="trace_logger.py", description="JSONL trace logger (see traces/TRACE_SPEC.md)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="write the opening record and print the trace id")
    s.add_argument("--stage", required=True)
    s.add_argument("--gate", required=True)
    s.add_argument("--role", required=True)
    s.add_argument("--instance", default="single")
    s.add_argument("--skill", required=True)
    s.add_argument("--prompt", required=True)
    s.add_argument("--model", required=True)
    s.add_argument("--settings", default="platform_default")
    s.add_argument("--inputs", nargs="*", default=[])
    s.add_argument("--parent")
    s.add_argument("--run", type=int, default=1)
    s.add_argument("--started-at", help="ISO 8601 override for started_at (retroactive records)")
    s.add_argument("--ended-at", help="ISO 8601 override written into the opening record (retroactive records only)")
    s.add_argument("--retroactive", action="store_true", help="record written after the fact; sets retroactive: true")

    e = sub.add_parser("end", help="complete a record")
    e.add_argument("--trace-id", required=True)
    e.add_argument("--outputs", nargs="*", default=[])
    e.add_argument("--selection", required=True, help="single_run | first_completed | best_of_n:<criterion>")
    e.add_argument("--human", default="none")
    e.add_argument("--safety-stop", action="store_true")
    e.add_argument("--safety-stop-subject", help="what was being processed when the safety stop fired")
    e.add_argument("--tool-calls", default='{"total": "not_exposed"}',
                   help='JSON object: {"total": N|"not_exposed", "by_tool": {"<tool>": N, ...}}')
    e.add_argument("--transcript", help="transcript file; copied to traces/transcripts/<trace_id>.<ext>")
    e.add_argument("--transcript-kind", choices=TRANSCRIPT_KINDS,
                   help="platform_export | final_report_only | none (default none; required with --transcript)")
    e.add_argument("--tokens-in")
    e.add_argument("--tokens-out")
    e.add_argument("--cost")
    e.add_argument("--discarded", help="reason the run was discarded or aborted (closes the record as discarded)")
    e.add_argument("--notes")
    e.add_argument("--started-at", help="ISO 8601 override for started_at")
    e.add_argument("--ended-at", help="ISO 8601 override for ended_at (default: now)")
    e.add_argument("--retroactive", action="store_true", help="record written after the fact; sets retroactive: true")

    c = sub.add_parser("check", help="list incomplete records (no ended_at) for a stage")
    c.add_argument("--stage", required=True)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    {"start": cmd_start, "end": cmd_end, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
