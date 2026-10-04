# Platform transcripts — Stage 1, session of 2026-10-04

Pushed at Sean Borycki's request on 2026-10-04 so the transcripts the charter requires for Stage 1 (trace capture, Stage 1 addition 1) outlive the session's temporary container. Copied unedited from the container's disk; snapshot taken 2026-10-04T16:09:26Z; first snapshot 2026-10-04T14:06:07Z. JSONL, one event per line, with full tool output; hashes are in `MANIFEST.sha256`.

| Folder | Contents |
|---|---|
| `head/` | The main session (head agent and Sean's messages) up to the snapshot time: `main-session.-home-user.jsonl`, `main-session.jsonl` (the session writes one file per working directory it has used). Includes the two exchanges Sean marked "inquiry, not for record"; he approved pushing them on 4 October |
| `reviewer/` | The independent reviewer: one agent resumed across passes 1 to 5, including the pass-3 run stopped by a rate limit |
| `round2-workflow/wf_740e44a5-0b1/` | The round-2 fix workflow: four fixers and five verifiers (`*.meta.json` names each one), `journal.jsonl` (each agent's returned result) and `workflow_script.js` (the orchestration script) |

`INDEX.md` maps each trace record to its transcript. Not here: the session that built the original Stage 1 zip, and the session that produced the research bundle; neither ran in this container.

TRACE_SPEC places transcripts at `traces/transcripts/<trace_id>.<ext>` and records them with `trace_logger.py end --transcript`. These records were completed before the transcripts were collected and records are never edited, so this branch and its index stand in for that until Sean sets the policy for later runs (OPEN_DECISIONS R-007).
