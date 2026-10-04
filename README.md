# Voluntary-control systematic review — Stage 1 build package

Program: the stage-gated research program in the Claude Research Team Plan (Gate 0 approved 2026-10-03; record in gate-packages/).
This package is the Stage 1 ("Team and tooling", weeks 1–2) build: the four agent skills, the master schema with mandatory provenance, the analysis scaffold, the trace specification, the reporting plan, the monitor specification and the dry-run protocol. It is meant to be opened as a project in Claude Code, where the Agent tool runs the specialist roles and CRAN is reachable.

## Folder map (matches the plan's Project folder structure)

| Folder | Holds |
|---|---|
| gate-packages/ | One file per gate: `G<n>_<date>_<title>.md`. Deliverable, verification note, reviewer report, open questions |
| skills/ | screening, extraction, appraisal, reviewer — each a SKILL.md with references/ |
| schema/ | master_extraction.csv (header), screening_decisions.csv, appraisal.csv, population_sd.csv, SCHEMA.md field dictionary |
| traces/ | TRACE_SPEC.md, trace_logger.py, and the JSONL traces + transcripts written by every agent run |
| analysis/ | R scaffold: setup.R, 00_load.R, 01_frequentist.R, 02_bayesian.R, 03_sof.R, run_all.R, ENVIRONMENT.md |
| reporting/ | REPORTING_PLAN.md (checklists and disclosure templates), METHODS_PAPER_OUTCOMES.md |
| monitor/ | MONITOR_SPEC.md — not created as a task until Gate 1 is approved |
| dry-run/ | DRY_RUN_PROTOCOL.md — the Gate 1 acceptance test |
| protocol/, searches/, screening/, extraction/, manuscript/ | Empty until their stage |

## Stage 1 status

| Gate 1 deliverable (plan) | File | Status |
|---|---|---|
| Screening skill | skills/screening/SKILL.md | Drafted; eligibility criteria marked DRAFT until Gate 2 registers them |
| Extraction skill | skills/extraction/SKILL.md | Drafted |
| Appraisal skill | skills/appraisal/SKILL.md | Drafted; uses the official RoB 2, ROBINS-I, JBI and GRADE documents, which are not reproduced here |
| Reviewer skill | skills/reviewer/SKILL.md | Drafted |
| Master CSV schema with provenance | schema/ | Drafted; analysis/00_load.R refuses rows with empty provenance |
| Pinned R environment | analysis/ENVIRONMENT.md, setup.R | Not pinned: this build sandbox has no R and cannot reach CRAN. Pin with renv in Claude Code at the dry run; commit renv.lock and session_info.txt |
| Project folder structure | this tree | Done |
| Monitor task specification | monitor/MONITOR_SPEC.md | Drafted |
| Dry run on five known studies | dry-run/DRY_RUN_PROTOCOL.md | Protocol written; run not executed (needs the Agent tool and full texts) |
| Trace capture (added at G0) | traces/ | Spec drafted; logger smoke-tested (start/end cycle, hashes, JSONL) |
| Reporting plan (added at G0) | reporting/ | Drafted |

## Running the dry run in Claude Code

1. Open this folder as the project. Install the four skills from skills/ (each folder is a skill).
2. `Rscript analysis/setup.R` then `renv::snapshot()`; commit renv.lock and analysis/session_info.txt.
3. Follow dry-run/DRY_RUN_PROTOCOL.md. Every agent run is logged with `python3 traces/trace_logger.py` before and after the run.
4. Assemble gate-packages/G1_<date>_team-and-tooling.md with the four parts the plan requires. Stop. Gate 1 is Sean's decision.

## Known tool limits carried from the plan

- Immune-challenge and endotoxin studies: extraction is done in the main session with Sean present, not in background agents (safety filters stopped two runs in the evidence review).
- Publisher sites that blocked fetches in the evidence review: ahajournals, Wiley, Taylor & Francis, Science. Sean retrieves those papers through institutional access and stages the PDFs under extraction/fulltext/.
- Crossref, OpenAlex and publisher pages rate-limit under bursts: query in batches of ten with a pause between batches. PubMed pages return no content to the fetch tool and are never used as a source; use the E-utilities API or Europe PMC instead.
