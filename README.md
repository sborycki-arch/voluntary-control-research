# Voluntary-control systematic review — Stage 1 build package (round 2)

Program: the stage-gated research program in the Claude Research Team Plan (Gate 0 approved by Sean on 2026-10-03; decision record in gate-packages/; Sean reported the trackers set to Approved on 2026-10-04).
This package is the Stage 1 ("Team and tooling", weeks 1–2) build: the four agent skills, the master schema with mandatory provenance, the analysis scaffold, the trace specification and logger, the reporting plan, the monitor specification and the dry-run protocol. Round 2 (2026-10-04) applied the builder-owned findings of the independent reviewer's register; CHANGELOG.md lists every change by register id, OPEN_DECISIONS.md lists what is left for Sean and the co-authors, and build-log/ holds the fixers' and verifiers' reports.

## Folder map

| Folder | Holds |
|---|---|
| gate-packages/ | One file per gate: `G<n>_<date>_<title>.md` (location and naming to be settled against the research repo, OPEN_DECISIONS R-048) |
| skills/ | screening, extraction, appraisal, reviewer — each a SKILL.md with references/ |
| schema/ | master_extraction.csv, screening_decisions.csv, appraisal.csv, population_sd.csv, grade_draft.csv, grade_final.csv (headers), SCHEMA.md field dictionary |
| tools/ | reconcile.py (A/B extraction diff, adjudication log, reconciled master), RECONCILIATION.md |
| traces/ | TRACE_SPEC.md, trace_logger.py, test_trace_logger.py, stage1.jsonl (every agent run so far), prompts/, transcripts/ |
| analysis/ | R scaffold: constants.R, 00_load.R, 01_effect_sizes.R, 02_frequentist.R, 03_bayesian.R, 04_sof.R, run_all.R, setup.R, ENVIRONMENT.md; synthetic/ (generator, synthetic masters, test suite) |
| reporting/ | REPORTING_PLAN.md, METHODS_PAPER_OUTCOMES.md, templates/ (header-only checklists) |
| monitor/ | MONITOR_SPEC.md — not created as a task until Gate 1 is approved |
| dry-run/ | DRY_RUN_PROTOCOL.md (the Gate 1 acceptance test), decoys.csv, selection.csv (header) |
| build-log/ | Round-2 fixer changelogs (CHANGELOG_A–D.md) and verifier reports (VERIFY_A–D.md, VERIFY_INTEGRATION.md) |
| protocol/, searches/, screening/, extraction/, manuscript/ | Empty until their stage |

## Stage 1 status after round 2

| Gate 1 deliverable (plan) | File | Status |
|---|---|---|
| Screening skill | skills/screening/SKILL.md | Drafted. DRAFT criteria admit validated pain ratings and seizure diaries (aligned to charter D2; confirm at G2). E7 (reviews) tested first; E6 is the head agent's; blind subset coded by the two co-authors |
| Extraction skill | skills/extraction/SKILL.md | Drafted. Blind human extraction subset (charter D4) added; `pre_post_r` recorded when printed; `is_primary_outcome` set at reconciliation |
| Appraisal skill | skills/appraisal/SKILL.md | Drafted. Field lists match schema/appraisal.csv and grade_draft.csv. Item lists, dual rating and adjudicator are Sean's decisions (R-044, R-045) |
| Reviewer skill | skills/reviewer/SKILL.md | Drafted; unchanged in round 2 |
| Master CSV schema with provenance | schema/, tools/ | Drafted. Loader refuses blank provenance, blank skill_version/model, out-of-vocabulary values and blank `is_primary_outcome` (executed). Reconciliation procedure and tool added |
| Pinned R or Python environment | analysis/ENVIRONMENT.md, setup.R | Not pinned. CRAN is blocked from the build environment; the scripts run on system R 4.3.3 (apt: metafor 4.4.0 and utilities) without bayesmeta or meta. The route is Sean's decision (R-038) |
| Project folder structure | this tree | Done (matches the plan's Stage 1 folder list; verified by the reviewer) |
| Monitor task specification | monitor/MONITOR_SPEC.md | Drafted. ClinicalTrials.gov API added; CENTRAL registered but not monitored (needs Cochrane Library access) |
| Dry run on five known studies | dry-run/DRY_RUN_PROTOCOL.md | Protocol revised; run not executed (full texts: only Kozhevnikov 2013 confirmed). Synthetic pooling-code test passes: `bash analysis/synthetic/run_synthetic_tests.sh` → 51 checks, 0 failures |
| Analysis scaffold | analysis/ | Raw master → effect sizes → frequentist → Bayesian (note rows without bayesmeta) → Summary of Findings runs end to end on synthetic data in the dry-run configuration (k = 1 everywhere) and the pooling configuration. Pre-Gate 5: the statistician co-author reviews every convention |
| Trace capture (added at G0) | traces/ | Spec and logger revised: locked, atomic writes; transcript, tool-call and retroactive fields; `python3 traces/test_trace_logger.py` → 45 checks, 0 failures. A retroactive record for the original build run exists (acceptance is Sean's, R-001) |
| Reporting plan (added at G0) | reporting/ | Drafted. Checklist templates are header-only until the primary standards documents are available (R-033, R-034, R-037) |

## Running the dry run in Claude Code

1. Open this folder as the project. Install the four skills from skills/ (each folder is a skill). The folder must be a git repository (skill hashes in traces come from git).
2. Environment on the route Sean chooses (analysis/ENVIRONMENT.md): `Rscript analysis/setup.R` on a CRAN-reachable machine, or the system-library route as documented.
3. `bash analysis/synthetic/run_synthetic_tests.sh` and `python3 traces/test_trace_logger.py` must both pass before any agent run.
4. Follow dry-run/DRY_RUN_PROTOCOL.md. Every agent run is logged with `python3 traces/trace_logger.py` before and after; concurrent runs are safe.
5. Assemble gate-packages/G1_<date>_team-and-tooling.md with the four parts the plan requires (deliverable, verification note, reviewer report, open questions). Stop. Gate 1 is Sean's decision.

## Known tool limits carried from the plan and the research document

- Immune-challenge and endotoxin studies (A09): extraction is done in the main session with Sean present, not in background agents (safety filters stopped two runs in the evidence review).
- Access failures recorded by the evidence review: ahajournals, Wiley, Taylor & Francis, Science and gastrojournal returned 403; PubMed pages returned no content; PNAS, PMC and JAMA Network intermittently served CAPTCHAs; Europe PMC, Crossref, OpenAlex, Semantic Scholar and ResearchGate rate-limited after a few requests. Sean retrieves blocked papers through institutional access and stages the PDFs under extraction/fulltext/.
- Crossref, OpenAlex and publisher pages: query in batches of ten with a pause between batches. PubMed pages are never used as a source; use the E-utilities API or Europe PMC instead.
- The build environment cannot reach CRAN, publisher sites or the standards hosts (JMIR, arXiv, OSF, doi.org); nothing from those sources was read during the build.
