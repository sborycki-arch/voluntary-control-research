# Changelog — Stage 1 package

Register ids refer to the independent reviewer's issues_register.csv (77 rows at the start of round 2). Per-area detail with commands and outputs: build-log/CHANGELOG_A–D.md; independent verification of each closure: build-log/VERIFY_A–D.md and VERIFY_INTEGRATION.md.

## Round 2 — 2026-10-04 (baseline commit d6306f3 = the delivered zip; contract 66351bd)

Authority: Sean, in the session, 2026-10-04: "G0 set to Approved in both trackers; proceed with builder fixes."

### Head agent
- R-004: package placed under git; skill_version hashes now resolve in trace records.
- Schema: master_extraction.csv gains `pre_post_r` and `is_primary_outcome` (BUILD_CONTRACT item 1).
- README.md rewritten for round 2; R-002 README claim replaced by the test suite reference; R-064 access list carried into README.
- Cross-area cleanup after integration verification: RECONCILIATION.md, SCHEMA.md and reconcile.py now state that 00_load.R refuses a blank `is_primary_outcome` (fail-closed) instead of warning; SCHEMA.md file count corrected (nine); synthetic GRADE certainty values title-cased to match SCHEMA (High/Moderate) and the suite assertion updated; dry-run pass criterion 1 and candidate-table notes no longer attribute dry-run target derivations to 01_effect_sizes.R; dry-run step 6 names the CRAN-reachable machine for setup.R; appraisal SKILL.md no longer uses "harvested only"; tool-sources.md marks the Minozzi 2020 figures unverified (R-036); extraction skill, screening skill and METHODS_PAPER_OUTCOMES agree that both co-authors code the blind subsets (charter D4); REPORTING_PLAN disclosure and methods sentence set include the blind human extraction subset (R-020); 04_sof.R `note` forced to character so a zero-effect-size run with a GRADE file no longer halts; 00_load.R requires `n_total`; 01_effect_sizes.R writes a header-only inputs file when nothing is computed; trace_logger.py preserves the stage file's mode on atomic replace.
- OPEN_DECISIONS.md written: every Sean/SME/statistician-owned row with current state and consequence.

### A — traces (fixer trace s1-builder-A-20261004T115625Z-3745; verifier s1-verifier-A-…-fe06)
- Closed: R-003, R-005, R-006, R-008, R-077 — locked, atomic logger (fcntl + temp file + os.replace); 3 × 20 interleaved start/end pairs and 60 concurrent ends lose nothing; id/file format in TRACE_SPEC matches the logger; `--tool-calls`, `--safety-stop-subject`, `--transcript`, `--started-at/--ended-at`, `--retroactive`, `check` subcommand; selection_policy validated; plain one-line errors, nothing written on error.
- Partial: R-001 — retroactive record for the original build run (`s1-head-single-20261004T120317Z-7a6b`, retroactive: true, outputs hashed against the zip 20/20); acceptance is Sean's. Its `agent_role` reads `head` while the stand-in prompt names a separate builder agent; records are never edited, so this stays as noted. R-002 — traces/test_trace_logger.py (45 checks). R-007 — transcript mechanism and spec section exist; no transcript has yet been attached to any run (policy question in OPEN_DECISIONS).

### B — analysis (fixer s1-builder-B-20261004T115643Z-7a57; verifier s1-verifier-B-…-8698)
- Closed: R-009 (01_effect_sizes.R: SMD/SMCR/PLO/OR/Z from the master, independently recomputed by the verifier), R-010 (freq_individual.csv for every row; k < 3 units reported individually), R-017, R-018 (vocabulary and provenance validation with reasons), R-067 (`meta` dropped), R-069 (SMCR with `pre_post_r` or the r = 0.5 placeholder and 0.3/0.7 sensitivity), R-070 (measure routing; only SMD-scale measures reach the SMD priors), R-072 (manifest excludes itself; CSVs then PNGs; byte-identical across runs), R-075 (dry-run configuration runs end to end; missing GRADE file degrades to empty columns).
- Partial: R-012 (pooling unit = ability × measure on primary rows; multilevel alternative is Gate 5), R-015 and R-076(b) (setup.R rewritten but not executable without CRAN), R-016 (bayesmeta guards executed; the bayesmeta-present branch exercised only with a stub).
- Scripts renumbered: 01_effect_sizes.R, 02_frequentist.R, 03_bayesian.R, 04_sof.R; constants.R added; analysis/synthetic/ added (generator, two synthetic masters, synthetic population SD and GRADE, run_synthetic_tests.sh: 51 checks).

### C — skills and schema (fixer s1-builder-C-20261004T120715Z-fd60; verifier s1-verifier-C-…-ae56)
- Closed: R-013 (grade_draft/grade_final headers and SCHEMA sections), R-014, R-019 (tools/reconcile.py diff/build with adjudication log; tested on every discrepancy type and the refusal), R-022 (harvest = exclude/E7; no `harvest` code value), R-024, R-055 (population_sd.csv: four DOIs added from the research document; Gatt et al. 2019 identified; A04 population cell changed to "young adults with typical hearing" and the SD caveat carried in notes; all rows stay pilot_unverified), R-057 (abilities.md crosswalk to evidence.csv ids and key sources, 26 = 26), R-073 (E7 first; E6 head-agent only).
- Partial: R-020 (blind human extraction subset procedure in the skill), R-068 (criteria redrafted to admit validated pain ratings and seizure diaries; scope ruling is Sean's at G2).

### D — dry run, reporting, monitor (fixer s1-builder-D-20261004T121652Z-bef3; verifier s1-verifier-D-…-636c)
- Closed: R-026, R-028 (protocol step; the synthetic suite is the pooling-code test), R-030 (decoys.csv: 10 out-of-scope records from the research document's reference list with expected codes), R-051, R-052 (Paravlic 2018 = screening E7 test case), R-053, R-054 (precision rule), R-064 (access plan).
- Partial: R-020 (outcomes #3/#4), R-031 (printed/derived marked; settled by the precision rule when full texts arrive), R-035, R-036, R-037 (need the primary documents).

### Not touched in round 2 (owner is Sean, the SME or the statistician)
R-021, R-023, R-025, R-027, R-029, R-032, R-033, R-034, R-038, R-040, R-041, R-043, R-044, R-045, R-046, R-047, R-048, R-049, R-050, R-056, R-058, R-059, R-060, R-061, R-062, R-063, R-065, R-066, R-071, R-074 — see OPEN_DECISIONS.md. Exception R-021: the screening skill's subset-coder sentence was changed to the charter's wording (co-authors code; Sean adjudicates); disclosed for Sean's confirmation.
