#!/usr/bin/env python3
"""Minimal JSONL trace logger for agent runs. Untested in the build sandbox; exercise in the dry run.
Usage:
  trace_logger.py start --stage 1 --gate G1 --role extraction --instance A --skill skills/extraction \
      --prompt traces/prompts/p.md --model "model-string" --inputs a.pdf b.pdf [--parent <trace_id>]
  trace_logger.py end --trace-id <id> --outputs out.csv --selection single_run --human none [--tokens-in N --tokens-out N --cost X]
"""
import argparse, hashlib, json, os, secrets, subprocess, sys
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()
def git_short(path):
    try:
        return subprocess.check_output(["git", "log", "-1", "--format=%h", "--", path], text=True).strip() or "untracked"
    except Exception:
        return "no_git"
def trace_path(stage): return os.path.join(os.path.dirname(__file__), f"stage{stage}.jsonl")

def start(a):
    tid = f"s{a.stage}-{a.role}-{a.instance}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(2)}"
    rec = {"trace_id": tid, "parent_trace_id": a.parent or "", "stage": a.stage, "gate": a.gate,
           "agent_role": a.role, "agent_instance": a.instance, "skill_name": os.path.basename(a.skill.rstrip("/")),
           "skill_version": git_short(a.skill), "prompt_ref": a.prompt, "prompt_sha256": sha(a.prompt),
           "model": a.model, "model_settings": a.settings, "started_at": now(), "ended_at": "",
           "input_refs": [{"path": p, "sha256": sha(p)} for p in a.inputs], "output_refs": [],
           "tool_calls": {}, "tokens_in": "", "tokens_out": "", "cost_usd": "",
           "run_number": a.run, "selection_policy": "", "discarded_reason": "",
           "human_intervention": "", "safety_stop": False, "notes": ""}
    with open(trace_path(a.stage), "a") as f: f.write(json.dumps(rec) + "\n")
    print(tid)

def end(a):
    stage = a.trace_id.split("-")[0][1:]
    path = trace_path(stage)
    recs = [json.loads(l) for l in open(path)]
    hit = [r for r in recs if r["trace_id"] == a.trace_id]
    if not hit: sys.exit(f"trace {a.trace_id} not found in {path}")
    r = hit[0]
    r.update({"ended_at": now(), "output_refs": [{"path": p, "sha256": sha(p)} for p in a.outputs],
              "selection_policy": a.selection, "human_intervention": a.human, "safety_stop": a.safety_stop,
              "tokens_in": a.tokens_in or "not_exposed", "tokens_out": a.tokens_out or "not_exposed",
              "cost_usd": a.cost or "not_exposed", "discarded_reason": a.discarded or "", "notes": a.notes or ""})
    with open(path, "w") as f:
        for x in recs: f.write(json.dumps(x) + "\n")
    print("completed", a.trace_id)

p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("start"); s.add_argument("--stage", required=True); s.add_argument("--gate", required=True)
s.add_argument("--role", required=True); s.add_argument("--instance", default="single"); s.add_argument("--skill", required=True)
s.add_argument("--prompt", required=True); s.add_argument("--model", required=True); s.add_argument("--settings", default="platform_default")
s.add_argument("--inputs", nargs="*", default=[]); s.add_argument("--parent"); s.add_argument("--run", type=int, default=1)
e = sub.add_parser("end"); e.add_argument("--trace-id", required=True); e.add_argument("--outputs", nargs="*", default=[])
e.add_argument("--selection", required=True); e.add_argument("--human", default="none"); e.add_argument("--safety-stop", action="store_true")
e.add_argument("--tokens-in"); e.add_argument("--tokens-out"); e.add_argument("--cost"); e.add_argument("--discarded"); e.add_argument("--notes")
a = p.parse_args(); start(a) if a.cmd == "start" else end(a)
