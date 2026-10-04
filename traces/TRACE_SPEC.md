# Trace specification

Every agent invocation in this program writes one JSON record to `traces/stage<N>.jsonl` (one file per stage, one JSON object per line) and, where a transcript can be captured, saves it as `traces/transcripts/<trace_id>.<ext>` (`.md`, `.json` or `.txt` as exported). The trace is the artefact that lets a reader re-run or audit a step; it is released at publication with the data and code, minus the full texts of paywalled papers.

## Record fields
| Field | Content |
|---|---|
| trace_id | `s<N>-<role>-<instance>-<YYYYMMDDTHHMMSSZ>-<4 random hex>`, e.g. `s1-extraction-A-20261004T120000Z-ab12`. `s<N>` is the stage; the logger derives the stage file from this prefix and rejects an id without it |
| parent_trace_id | head-agent trace that launched this run, or blank |
| stage, gate | Stage number (string, as in the id) and the gate it feeds |
| agent_role | `head`, `builder`, `verifier`, `search`, `screening`, `extraction`, `appraisal`, `statistician`, `reviewer`, `citation`, `writer`, `monitor` |
| agent_instance | `A`, `B`, `single`, or a fixer letter for builder runs |
| skill_name, skill_version | skill folder name and git short hash of the last commit touching the skill folder at run time; `untracked` if the folder is not committed, `no_git` outside a repository, `not_recorded` if the path does not exist (retroactive records) |
| prompt_ref, prompt_sha256 | path to the exact prompt text given to the agent and its sha256 |
| model | exact model identifier string reported by the platform; `not_recorded` only in retroactive records |
| model_settings | temperature or other settings if exposed; `platform_default` otherwise |
| started_at, ended_at | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`); set by the logger clock unless overridden with `--started-at` / `--ended-at` (offsets are normalised to UTC) |
| input_refs | list of `{path, sha256}` for every file the agent was given |
| output_refs | list of `{path, sha256}` for every file the agent produced |
| tool_calls | JSON object `{"total": <int or "not_exposed">, "by_tool": {"<tool>": <int>, ...}}`; `{"total": "not_exposed"}` when the platform does not expose counts; `{}` only in an unfinished record |
| tokens_in, tokens_out, cost_usd | from the platform if available; `not_exposed` otherwise |
| run_number, selection_policy | which attempt this is and how the kept run was chosen: `single_run`, `first_completed`, or `best_of_n:<criterion>` (e.g. `best_of_n:fewest_unsure`); the logger rejects any other value. Discarded runs are logged too, with `discarded_reason` |
| discarded_reason | blank, or why the run was discarded or aborted (rate limit, safety stop, superseded by a re-run) |
| human_intervention | `none`, `adjudicated_by_sean`, `edited_by_<initials>`, `rerun_after_safety_stop` |
| safety_stop, safety_stop_subject | `true`/`false`; if true, `safety_stop_subject` names what was being processed (record id, file, topic). A safety stop without a subject is recorded as `not_recorded` with a warning |
| transcript_ref, transcript_sha256, transcript_kind | path `traces/transcripts/<trace_id>.<ext>` and its sha256 when a transcript was captured; `transcript_kind` is `platform_export`, `final_report_only` or `none` (see Transcript capture) |
| retroactive | `false` for a record opened before the run; `true` when the record was written after the fact (either subcommand's `--retroactive`). A retroactive record is evidence that a run happened, not a trace of it; its acceptance is a gate decision |
| notes | free text |

## Rules
- The record is written before the run (`started_at`, inputs, prompt hash) and completed after it (`ended_at`, outputs, selection). A run without a completed record is treated as not having happened. `trace_logger.py check --stage <N>` lists the records still open.
- Discarded or aborted runs (rate limit, crash, safety stop, superseded attempt) are still closed with `end`, with `--discarded "<reason>"` and, where it applies, `--safety-stop --safety-stop-subject "<what>"`; they are never deleted or left open.
- Prompts are stored verbatim under `traces/prompts/` and never edited after use; a changed prompt is a new file and a new skill version.
- Head-agent planning turns are traced like any other run. Builder (fix) runs and verifier runs are traced with roles `builder` and `verifier`.
- Existing records are never edited by hand. The only write paths are the logger's `start` (append) and `end` (complete one record).
- The release package at Gate 7 includes `traces/*.jsonl`, `traces/prompts/`, `traces/transcripts/` and a `MANIFEST.sha256`.

## Transcript capture (Claude Code)
The platform does not hand a sub-agent its own transcript. The head agent that launched the run captures it at `end` time, as one of three kinds:
- `platform_export` — the platform's per-agent transcript file (the JSONL/Markdown export of that agent's turn) when the head agent can reach it on disk or via an export action. Pass it with `--transcript <file> --transcript-kind platform_export`; the logger copies it to `traces/transcripts/<trace_id>.<ext>` and records its sha256.
- `final_report_only` — when no transcript file is reachable, the head agent saves the agent's hand-back text (its final report or structured output) verbatim to a file and passes that with `--transcript-kind final_report_only`. This captures what the agent returned, not how it got there, and the record says so.
- `none` — no transcript captured. This is the default, and it is the normal state of the head agent's own turn unless the session export is attached afterwards. A record with `none` is complete but not fully auditable; the Gate 7 release lists such records.
The transcript file is copied, not moved; the original stays where the platform put it. `--transcript` without `--transcript-kind` is rejected so that the kind is always a deliberate statement.

## Locking and atomicity
All logger processes serialise on the lock file `traces/.lock` with `fcntl.flock` (exclusive) for every read-modify-write: `start` appends under the lock; `end` reads the whole stage file, modifies one record and rewrites the file to a temporary file in the same directory, then `os.replace`s it over the original, all under the lock. Interleaved `start`/`end` calls from many processes therefore lose no record and never leave a torn line (tested: 3 trials x 20 concurrent start->end pairs, `traces/test_trace_logger.py`). Callers may additionally wrap a call in `flock traces/.lock <command>`; the logger detects the inherited lock descriptor and reuses it instead of deadlocking against it. The lock file is not part of the package (`.gitignore`). A torn or hand-edited line in a stage file is reported by file and line number with exit 2; it must be repaired before the logger will write to that file again.

## Logger
`traces/trace_logger.py` (Python 3 standard library only). Exit codes: 0 success; 2 for a validation or usage error (plain one-line message on stderr, nothing written): missing prompt, input, output or transcript path, invalid `--selection`, invalid `--tool-calls` JSON, malformed trace id, unknown trace id, bad timestamp, torn stage file.

- Open a record: `python3 traces/trace_logger.py start --stage 1 --gate G1 --role extraction --instance A --skill skills/extraction --prompt traces/prompts/extraction_A_dryrun.md --model "<model string>" --inputs extraction/fulltext/x.pdf [--parent <trace_id>] [--run N] [--settings S]` prints the trace_id.
- Complete it: `python3 traces/trace_logger.py end --trace-id <id> --outputs extraction/dryrun_A.csv --selection single_run --human none [--tool-calls '{"total": 12, "by_tool": {"read": 9, "shell": 3}}'] [--transcript <file> --transcript-kind platform_export|final_report_only] [--tokens-in N --tokens-out N --cost X] [--notes "<text>"]`.
- Close a discarded run: `... end --trace-id <id> --selection single_run --discarded "<reason>" [--safety-stop --safety-stop-subject "<what>"]`.
- Retroactive record: `start ... --retroactive --started-at 2026-10-04T03:34:00Z` then `end ... --retroactive --ended-at 2026-10-04T03:41:00Z`. `--started-at` / `--ended-at` are also accepted on `end` to correct the clock of a record opened late.
- Open records: `python3 traces/trace_logger.py check --stage 1`.
- Tests: `python3 traces/test_trace_logger.py` runs in a temporary directory and exits 0 on pass (sequential cycle with hashlib verification, 3 x 20 concurrent pairs, retroactive record, transcript copy, invalid selection, missing files, malformed id, flock wrapper, torn line).
