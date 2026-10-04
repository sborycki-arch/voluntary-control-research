# Trace specification

Every agent invocation in this program writes one JSON record to `traces/<stage>.jsonl` and saves its raw transcript to `traces/transcripts/<trace_id>.md` (or .json as exported). The trace is the artefact that lets a reader re-run or audit a step; it is released at publication with the data and code, minus the full texts of paywalled papers.

## Record fields
| Field | Content |
|---|---|
| trace_id | `<stage>-<role>-<instance>-<YYYYMMDDTHHMMSSZ>-<4 random hex>` |
| parent_trace_id | head-agent trace that launched this run, or blank |
| stage, gate | Stage number and the gate it feeds |
| agent_role | `head`, `search`, `screening`, `extraction`, `appraisal`, `statistician`, `reviewer`, `citation`, `writer`, `monitor` |
| agent_instance | `A`, `B`, or `single` |
| skill_name, skill_version | skill folder name and git short hash of the skill at run time |
| prompt_ref, prompt_sha256 | path to the exact prompt text given to the agent and its hash |
| model | exact model identifier string reported by the platform |
| model_settings | temperature or other settings if exposed; `platform_default` otherwise |
| started_at, ended_at | ISO 8601 UTC |
| input_refs | list of `{path, sha256}` for every file the agent was given |
| output_refs | list of `{path, sha256}` for every file the agent produced |
| tool_calls | count, and counts by tool (web_fetch, file read, shell) |
| tokens_in, tokens_out, cost_usd | from the platform if available; blank with `not_exposed` otherwise |
| run_number, selection_policy | which attempt this is and how the kept run was chosen (`single_run`; `first_completed`; `best_of_n:<criterion>` with n). Discarded runs are logged too, with `discarded_reason` |
| human_intervention | `none`, `adjudicated_by_sean`, `edited_by_<initials>`, `rerun_after_safety_stop` |
| safety_stop | `true`/`false`; if true, what was being processed |
| notes | free text |

## Rules
- The record is written before the run (`started_at`, inputs, prompt hash) and completed after it (`ended_at`, outputs, selection). A run without a completed record is treated as not having happened.
- Prompts are stored verbatim under `traces/prompts/` and never edited after use; a changed prompt is a new file and a new skill version.
- Head-agent planning turns are traced like any other run.
- The release package at Gate 7 includes `traces/*.jsonl`, `traces/prompts/`, `traces/transcripts/` and a `MANIFEST.sha256`.

## Logger
`python3 traces/trace_logger.py start --stage 1 --gate G1 --role extraction --instance A --skill skills/extraction --prompt traces/prompts/extraction_A_dryrun.md --model "<model string>" --inputs extraction/fulltext/x.pdf` prints a trace_id and writes the opening record.
`python3 traces/trace_logger.py end --trace-id <id> --outputs extraction/dryrun_A.csv --selection single_run --human none` completes it.
