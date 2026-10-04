#!/usr/bin/env python3
"""Tests for traces/trace_logger.py. Standard library only; runs in a fresh temporary directory; exit 0 on pass.

Usage: python3 traces/test_trace_logger.py [path/to/logger.py]
       (default: the trace_logger.py next to this file)

The logger under test is copied to <tmp>/pkg/traces/trace_logger.py so that its stage files, lock
file and transcripts folder are created under the temporary directory, never in the package.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER_SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "trace_logger.py")
FAILURES = []


def check(cond, msg):
    status = "ok  " if cond else "FAIL"
    print(f"[{status}] {msg}")
    if not cond:
        FAILURES.append(msg)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(args, cwd, timeout=60):
    return subprocess.run([PY, "traces/trace_logger.py", *args], cwd=cwd, text=True,
                          capture_output=True, timeout=timeout)


def records(stage_file):
    recs, torn = [], 0
    if not os.path.exists(stage_file):
        return recs, torn
    for line in open(stage_file, encoding="utf-8"):
        if not line.strip():
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            torn += 1
    return recs, torn


def main():
    tmp = tempfile.mkdtemp(prefix="trace_logger_test_")
    pkg = os.path.join(tmp, "pkg")
    traces = os.path.join(pkg, "traces")
    os.makedirs(os.path.join(traces, "prompts"))
    shutil.copyfile(LOGGER_SRC, os.path.join(traces, "trace_logger.py"))
    print(f"logger under test: {LOGGER_SRC}\ntemp dir: {tmp}")

    prompt = os.path.join(traces, "prompts", "p.md")
    open(prompt, "w").write("prompt text\n")
    inp = os.path.join(pkg, "input.csv")
    open(inp, "w").write("a,b\n1,2\n")
    out = os.path.join(pkg, "output.csv")
    open(out, "w").write("x\n3\n")
    transcript = os.path.join(pkg, "transcript.md")
    open(transcript, "w").write("# transcript\nhello\n")
    stage1 = os.path.join(traces, "stage1.jsonl")

    # 1. sequential start -> end cycle, sha256 verified against hashlib
    r = run(["start", "--stage", "1", "--gate", "G1", "--role", "extraction", "--instance", "A",
             "--skill", "skills/extraction", "--prompt", "traces/prompts/p.md", "--model", "m",
             "--inputs", "input.csv"], pkg)
    check(r.returncode == 0, f"start exits 0 (stderr: {r.stderr.strip()[:200]})")
    tid = r.stdout.strip()
    check(tid.startswith("s1-extraction-A-"), f"start prints trace id with s1- prefix: {tid}")
    recs, torn = records(stage1)
    check(len(recs) == 1 and torn == 0, "one valid record after start")
    rec = recs[0]
    check(rec["prompt_sha256"] == sha(prompt), "prompt sha256 matches hashlib")
    check(rec["input_refs"] == [{"path": "input.csv", "sha256": sha(inp)}], "input sha256 matches hashlib")
    check(rec["ended_at"] == "" and rec["retroactive"] is False, "start record is open and not retroactive")
    for k in ("safety_stop_subject", "transcript_ref", "transcript_sha256", "transcript_kind", "retroactive"):
        check(k in rec, f"start record carries field {k}")
    r = run(["check", "--stage", "1"], pkg)
    check(r.returncode == 0 and "1 incomplete" in r.stdout and tid in r.stdout, "check lists the open record")

    r = run(["end", "--trace-id", tid, "--outputs", "output.csv", "--selection", "single_run", "--human", "none",
             "--tool-calls", '{"total": 5, "by_tool": {"read": 3, "shell": 2}}', "--notes", "seq test"], pkg)
    check(r.returncode == 0 and r.stdout.strip() == f"completed {tid}", f"end exits 0 and prints completed (stderr: {r.stderr.strip()[:200]})")
    recs, torn = records(stage1)
    rec = recs[0]
    check(len(recs) == 1 and torn == 0, "still one valid record after end")
    check(rec["output_refs"] == [{"path": "output.csv", "sha256": sha(out)}], "output sha256 matches hashlib")
    check(rec["ended_at"] != "" and rec["selection_policy"] == "single_run", "end fills ended_at and selection_policy")
    check(rec["tool_calls"] == {"total": 5, "by_tool": {"read": 3, "shell": 2}}, "tool_calls JSON stored")
    check(rec["tokens_in"] == "not_exposed" and rec["transcript_kind"] == "none", "defaults: tokens not_exposed, transcript_kind none")
    r = run(["check", "--stage", "1"], pkg)
    check(r.returncode == 0 and "0 incomplete" in r.stdout, "check reports 0 incomplete after end")

    # default tool_calls when the option is absent
    r = run(["start", "--stage", "1", "--gate", "G1", "--role", "screening", "--skill", "skills/screening",
             "--prompt", "traces/prompts/p.md", "--model", "m"], pkg)
    tid2 = r.stdout.strip()
    r = run(["end", "--trace-id", tid2, "--selection", "first_completed"], pkg)
    rec2 = [x for x in records(stage1)[0] if x["trace_id"] == tid2][0]
    check(r.returncode == 0 and rec2["tool_calls"] == {"total": "not_exposed"}, "tool_calls default is {\"total\": \"not_exposed\"}")
    r = run(["start", "--stage", "1", "--gate", "G1", "--role", "screening", "--skill", "skills/screening",
             "--prompt", "traces/prompts/p.md", "--model", "m"], pkg)
    tid3 = r.stdout.strip()
    r = run(["end", "--trace-id", tid3, "--selection", "best_of_n:fewest_unsure", "--safety-stop",
             "--safety-stop-subject", "record 17 (self-harm content)", "--discarded", "aborted after safety stop"], pkg)
    rec3 = [x for x in records(stage1)[0] if x["trace_id"] == tid3][0]
    check(r.returncode == 0 and rec3["safety_stop"] is True and rec3["safety_stop_subject"] == "record 17 (self-harm content)"
          and rec3["discarded_reason"] == "aborted after safety stop" and rec3["selection_policy"] == "best_of_n:fewest_unsure",
          "safety stop subject, discarded reason and best_of_n:<criterion> recorded")

    # 2. concurrency: 3 trials x 20 interleaved start->end pairs
    worker = os.path.join(tmp, "worker.py")
    open(worker, "w").write(
        "import subprocess, sys\n"
        "py, stage, n = sys.argv[1], sys.argv[2], sys.argv[3]\n"
        "r = subprocess.run([py, 'traces/trace_logger.py', 'start', '--stage', stage, '--gate', 'G1', '--role', 'worker',\n"
        "    '--instance', n, '--skill', 'skills/x', '--prompt', 'traces/prompts/p.md', '--model', 'm', '--inputs', 'input.csv'],\n"
        "    text=True, capture_output=True)\n"
        "if r.returncode != 0: sys.exit('start failed: ' + r.stderr)\n"
        "tid = r.stdout.strip()\n"
        "r = subprocess.run([py, 'traces/trace_logger.py', 'end', '--trace-id', tid, '--outputs', 'output.csv',\n"
        "    '--selection', 'single_run', '--human', 'none', '--notes', 'worker ' + n], text=True, capture_output=True)\n"
        "if r.returncode != 0: sys.exit('end failed: ' + r.stderr)\n"
    )
    for trial in (1, 2, 3):
        stage = str(10 + trial)
        stage_file = os.path.join(traces, f"stage{stage}.jsonl")
        procs = [subprocess.Popen([PY, worker, PY, stage, str(i)], cwd=pkg, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(20)]
        failed_ends = 0
        for p in procs:
            _, err = p.communicate(timeout=300)
            if p.returncode != 0:
                failed_ends += 1
                print("   worker error:", err.strip()[:200])
        recs, torn = records(stage_file)
        complete = [x for x in recs if x.get("ended_at")]
        check(len(recs) == 20 and len(complete) == 20 and torn == 0 and failed_ends == 0,
              f"trial {trial}: {len(recs)} records, {len(complete)} complete, {torn} torn lines, {failed_ends} failed ends")

    # 3. retroactive record with time overrides
    r = run(["start", "--stage", "2", "--gate", "G1", "--role", "head", "--instance", "single", "--skill", "skills",
             "--prompt", "traces/prompts/p.md", "--model", "not_recorded", "--retroactive",
             "--started-at", "2026-10-04T03:34:00Z"], pkg)
    rtid = r.stdout.strip()
    check(r.returncode == 0 and rtid.startswith("s2-head-single-"), "retroactive start accepted")
    r = run(["end", "--trace-id", rtid, "--outputs", "output.csv", "--selection", "single_run", "--retroactive",
             "--ended-at", "2026-10-04T03:41:00Z", "--notes", "retro"], pkg)
    rrec = records(os.path.join(traces, "stage2.jsonl"))[0][0]
    check(r.returncode == 0 and rrec["retroactive"] is True and rrec["started_at"] == "2026-10-04T03:34:00Z"
          and rrec["ended_at"] == "2026-10-04T03:41:00Z", "retroactive record carries retroactive: true and the override times")
    r = run(["end", "--trace-id", rtid, "--selection", "single_run", "--ended-at", "2026-10-04 bad"], pkg)
    check(r.returncode == 2 and "ISO 8601" in r.stderr and "Traceback" not in r.stderr, "bad --ended-at rejected with exit 2")
    r = run(["end", "--trace-id", rtid, "--selection", "single_run", "--ended-at", "2026-10-04T05:41:00+02:00"], pkg)
    rrec = records(os.path.join(traces, "stage2.jsonl"))[0][0]
    check(r.returncode == 0 and rrec["ended_at"] == "2026-10-04T03:41:00Z", "offset timestamp normalised to UTC Z")

    # 4. transcript copy
    r = run(["start", "--stage", "3", "--gate", "G1", "--role", "appraisal", "--instance", "B", "--skill", "skills/appraisal",
             "--prompt", "traces/prompts/p.md", "--model", "m"], pkg)
    ttid = r.stdout.strip()
    r = run(["end", "--trace-id", ttid, "--selection", "single_run", "--transcript", "transcript.md"], pkg)
    check(r.returncode == 2 and "transcript-kind" in r.stderr, "--transcript without --transcript-kind rejected (exit 2)")
    r = run(["end", "--trace-id", ttid, "--selection", "single_run", "--transcript", "transcript.md",
             "--transcript-kind", "platform_export"], pkg)
    dest = os.path.join(traces, "transcripts", f"{ttid}.md")
    trec = records(os.path.join(traces, "stage3.jsonl"))[0][0]
    check(r.returncode == 0 and os.path.isfile(dest) and sha(dest) == sha(transcript), "transcript copied to traces/transcripts/<trace_id>.md")
    check(trec["transcript_ref"] == f"traces/transcripts/{ttid}.md" and trec["transcript_sha256"] == sha(transcript)
          and trec["transcript_kind"] == "platform_export", "transcript_ref, sha256 and kind recorded")
    r = run(["end", "--trace-id", ttid, "--selection", "single_run", "--transcript", "missing.md",
             "--transcript-kind", "final_report_only"], pkg)
    check(r.returncode == 2 and "missing.md" in r.stderr, "missing transcript rejected (exit 2)")

    # 5. invalid selection rejected, record untouched
    before = open(stage1, "rb").read()
    r = run(["end", "--trace-id", tid, "--selection", "best_guess"], pkg)
    check(r.returncode == 2 and "--selection" in r.stderr and "Traceback" not in r.stderr, "invalid selection exits 2 with a plain message")
    check(open(stage1, "rb").read() == before, "invalid selection writes nothing")
    r = run(["end", "--trace-id", tid, "--selection", "best_of_n:"], pkg)
    check(r.returncode == 2, "best_of_n without criterion rejected")

    # 6. missing files rejected, nothing written
    r = run(["start", "--stage", "4", "--gate", "G1", "--role", "x", "--skill", "s", "--prompt", "traces/prompts/p.md",
             "--model", "m", "--inputs", "input.csv", "nope.pdf"], pkg)
    check(r.returncode == 2 and "nope.pdf" in r.stderr and "Traceback" not in r.stderr, "missing input exits 2 with a plain message")
    check(not os.path.exists(os.path.join(traces, "stage4.jsonl")), "missing input writes nothing")
    r = run(["start", "--stage", "4", "--gate", "G1", "--role", "x", "--skill", "s", "--prompt", "traces/prompts/absent.md",
             "--model", "m"], pkg)
    check(r.returncode == 2 and "absent.md" in r.stderr, "missing prompt exits 2")
    before = open(stage1, "rb").read()
    r = run(["end", "--trace-id", tid, "--selection", "single_run", "--outputs", "output.csv", "gone.csv"], pkg)
    check(r.returncode == 2 and "gone.csv" in r.stderr and "Traceback" not in r.stderr, "missing output exits 2 with a plain message")
    check(open(stage1, "rb").read() == before, "missing output writes nothing")

    # 7. malformed trace id, unknown trace id, bad JSON
    r = run(["end", "--trace-id", "1-extraction-A-x-ab12", "--selection", "single_run"], pkg)
    check(r.returncode == 2 and "malformed trace id" in r.stderr, "trace id without s<N>- prefix rejected")
    r = run(["end", "--trace-id", "s1-nobody-A-20260101T000000Z-0000", "--selection", "single_run"], pkg)
    check(r.returncode == 2 and "not found" in r.stderr, "unknown trace id exits 2")
    r = run(["end", "--trace-id", tid, "--selection", "single_run", "--tool-calls", "{not json"], pkg)
    check(r.returncode == 2 and "tool-calls" in r.stderr, "invalid --tool-calls JSON rejected")

    # 8. no deadlock under an external `flock traces/.lock` wrapper (the convention used by callers)
    if shutil.which("flock"):
        try:
            r = subprocess.run(["flock", "traces/.lock", PY, "traces/trace_logger.py", "start", "--stage", "5", "--gate", "G1",
                                "--role", "x", "--skill", "s", "--prompt", "traces/prompts/p.md", "--model", "m"],
                               cwd=pkg, text=True, capture_output=True, timeout=30)
            ftid = r.stdout.strip()
            r2 = subprocess.run(["flock", "traces/.lock", PY, "traces/trace_logger.py", "end", "--trace-id", ftid,
                                 "--selection", "single_run"], cwd=pkg, text=True, capture_output=True, timeout=30)
            check(r.returncode == 0 and r2.returncode == 0, "start/end complete under an external flock wrapper (no deadlock)")
        except subprocess.TimeoutExpired:
            check(False, "start/end under external flock wrapper timed out (deadlock)")
    else:
        print("[skip] flock(1) not available; wrapper test skipped")

    # 9. torn legacy line is reported, not a traceback
    stage6 = os.path.join(traces, "stage6.jsonl")
    open(stage6, "w").write('{"trace_id": "s6-a-b-c-d", "ended_at": ""}\n{"trace_id": "s6-torn\n')
    r = run(["check", "--stage", "6"], pkg)
    check(r.returncode == 2 and "line 2" in r.stderr and "Traceback" not in r.stderr, "torn line reported with its line number")

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(FAILURES)} failure(s)")
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
