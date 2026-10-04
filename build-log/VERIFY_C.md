# VERIFY_C — adversarial verification of fixer C (skills and schema), round-2 build, 2026-10-04

Verifier trace: `s1-verifier-C-20261004T122922Z-ae56` (prompt `traces/prompts/verify_C_2026-10-04.md`, inputs CHANGELOG_C.md). Fixer trace checked: `s1-builder-C-20261004T120715Z-fd60`. Everything below was executed in this environment (R 4.3.3, metafor 4.4.0, no bayesmeta, Python 3 stdlib) unless marked "read".

## Trace and prompt of the fixer
- `python3 traces/trace_logger.py check --stage 1` → "13 records, 3 incomplete": head-single-115033, verifier-B, verifier-C (mine, open at that moment). The builder-C record is complete: `started_at 2026-10-04T12:07:15Z`, `ended_at 2026-10-04T12:17:06Z`, `selection_policy single_run`, `human_intervention none`, 2 input_refs, 12 output_refs.
- `traces/prompts/fix_C_2026-10-04.md` exists (9166 bytes); its sha256 `e137c2f5…315a` equals the record's `prompt_sha256`.
- All 12 `output_refs` sha256 values recomputed → every one matches the file on disk now (nobody has touched C's files since the record was written).

## Working tree vs 66351bd
`git diff 66351bd --stat` → 20 files, 843+/266−; `git status --porcelain` → the modified/untracked list in the appendix. Restricted to C's ownership column (`git status --porcelain -- skills schema tools`): ` M schema/SCHEMA.md`, ` M schema/population_sd.csv`, ` M skills/appraisal/SKILL.md`, ` M skills/extraction/SKILL.md`, ` M skills/screening/SKILL.md`, ` M skills/screening/references/abilities.md`, `?? schema/grade_draft.csv`, `?? schema/grade_final.csv`, `?? tools/`. Exactly the files CHANGELOG_C.md lists; `skills/reviewer/` untouched (`git diff 66351bd --stat -- skills/reviewer` empty); `schema/master_extraction.csv`, `schema/screening_decisions.csv`, `schema/appraisal.csv` unchanged. Nothing committed.

## Per-id verdicts

### R-013 — grade_draft.csv / grade_final.csv schema: CLOSED
- `cat schema/grade_draft.csv` = `ability_id,outcome,…,skill_version,model` (21 columns, one line, trailing `\n`); python compare against the contract item 6 string with spaces removed → `draft match True`; `grade_final` = draft + `final_certainty,final_rater_id,final_date,change_reason,signed` → `final match True` (26 columns).
- `analysis/04_sof.R:16 grade_cols` = ability_id, outcome, n_studies, n_participants, final_certainty, reasons, plain_language_statement — all present in the header; join is `by = c("ability_id","outcome")` (line 35); `signed` column is checked (line 34).
- Executed: scratch copy of analysis/ + schema/, `VCR_IGNORE_RENV=1 VCR_MASTER=analysis/synthetic/master_pooling.csv VCR_GRADE_FINAL=schema/grade_final.csv Rscript analysis/run_all.R` → exit 0, "Summary of Findings: 4 rows (4 pooled, 0 individual); GRADE from schema/grade_final.csv" (header-only template joins cleanly, note "no grade_final row for this ability_id + outcome"); with `VCR_GRADE_FINAL=analysis/synthetic/grade_final_synthetic.csv` (B's 26-column file, same header) → exit 0, final_certainty populated.
- SCHEMA.md §grade_draft.csv / §grade_final.csv define every field; `outcome` = primary row's `outcome_measure` string. Appraisal skill line 34 now lists the 21 draft columns (python: list == header, True).
- Nit (not refuting): SCHEMA.md:3 says "defines seven of them" but lists six named files plus three reconciliation files.

### R-014 — appraisal Output field list: CLOSED
- Python: list parsed from `skills/appraisal/SKILL.md:20` == `schema/appraisal.csv` header → True, 12 fields, `notes` last. `git diff 66351bd --stat skills/appraisal/SKILL.md` → 2 insertions, 2 deletions (lines 20 and 34 only); R-044/R-045/R-071 text untouched.

### R-019 — reconciliation defined: CLOSED (one false statement to correct, below)
Re-ran every fixer test on copies of the fixtures (`scratchpad/verify_C_test`), results identical to CHANGELOG_C.md: `diff` → exit 0, 9 discrepancies (missing_in_A 2, missing_in_B 3, numeric 2, text 1, provenance 1), `5` vs `5.0` not reported; `build` with empty log → exit 2, nine named lines, "refusing to build: 9 of 9", no file; partial log → exit 2 naming D-0009; malformed log → exit 2, five named problems with line numbers; full log without `--primary` → exit 0 + warning, blank column; with `--primary` → exit 0, `yes` on the two finger-skin-temperature rows, `no` elsewhere, `extractor_id = reconciled`, `model = A=model-A;B=model-B`, 27.1 / 0.65 / merged notes applied; `A_dup.csv` → exit 2 with both line numbers; `py_compile` clean.
My own tests (`scratchpad/verify_C_test2`): output header == schema/master_extraction.csv header (True); `skill_version` merged `A=h1;B=h2`; key field containing `|` → exit 2 named; A/B header mismatch → warning + `missing_in_B`; duplicate log id → exit 2 "already adjudicated on line 2"; log lacking `chosen_value` column → exit 2; non-ISO date → exit 2; primary file with two outcomes for one study × ability → exit 2; `is_primary_outcome` written by an extractor is reported as a discrepancy (then overwritten by `--primary`). From the package root, `VCR_MASTER=../reconcile_test/master_reconciled.csv Rscript analysis/00_load.R` → exit 0, "Loaded 5 rows, 2 abilities … 0 verified population-SD rows (of 7)".
RECONCILIATION.md gives roles, procedure, log schema, what is compared, human-subset comparison, loader hand-off; SCHEMA.md §Reconciliation files matches the code's column lists (`DISCREPANCY_COLUMNS`, `LOG_COLUMNS`, `PRIMARY_COLUMNS`). The register's four asks (diff method, discrepancy-list format, adjudication-log format, reconciled-file production) are all met and executed.
- DEFECT (fix before the dry run, one sentence in two C-owned files): `tools/RECONCILIATION.md:35` and `schema/SCHEMA.md:102` say that without `--primary` the column "is left blank … with a warning, and nothing enters pooling (analysis/00_load.R warns per study × ability)". Executed: `VCR_MASTER=../reconcile_test/master_noprimary.csv Rscript analysis/00_load.R` → **"Error: 5 row(s) refused for controlled-vocabulary violations"**, reason `is_primary_outcome='' not in {yes|no}`, execution halted. The loader refuses, it does not warn. The fixer never ran the loader on the no-primary output. (Behaviour is fail-closed and consistent with SCHEMA's `yes`/`no` vocabulary; the prose is wrong.)
- Edge (note): `as_number` strips thousands commas, so `1,5` (European decimal) and `15` compare equal and are not reported; `92,457` vs `92457` equal (intended).

### R-020 (extraction-skill part) — blind human extraction subset: PARTIAL (as the fixer says)
- Read: `skills/extraction/SKILL.md:37-38` "Blind human subset (charter D4)": seeded 10–20% of included studies, `extractor_id = human-<initials>`, blind to agent files, Sean adjudicates and does not extract, comparison via `reconcile.py diff`, feeds METHODS_PAPER_OUTCOMES #4; `tools/RECONCILIATION.md:37-38` gives the command. The diff mechanism was executed (above). Fixer D's METHODS_PAPER_OUTCOMES.md #4 now carries the matching agent–human wording.
- Not closed: (a) the register asks for agent-vs-human **κ**; the skill yields exact-agreement and numeric-discrepancy rates, and whether κ is required is Sean's (reviewer Q5, pass-2 Q7); (b) charter D4 says both co-authors code the subset ("they code the blind 10–20% human subset"); the screening skill now says "the two human co-authors", the extraction skill says "a human co-author (the statistician or the subject-matter co-author)" — the two skills read D4 differently. Sean/head agent to settle with R-021/R-060.

### R-022 — harvest coding: CLOSED
- `grep -rn -i harvest skills schema tools` → three hits: `screening/SKILL.md:24` (rule 6: "`harvest` is not a code value and must not appear in `decision` or `exclusion_code`"), `SCHEMA.md:53` ("There is no `harvest` code value"; PRISMA-flow treatment stated), `appraisal/SKILL.md:15` "(harvested only)" — prose, not a code value. Decision for a review is stated as `exclude`/`E7` in rule 3, rule 6, the Design bullet, the code list and SCHEMA §screening_decisions.csv; κ computed on `decision` and `exclusion_code` (SCHEMA:56). `schema/screening_decisions.csv` header unchanged.
- Residual in a C-owned file: `skills/appraisal/SKILL.md:15` still uses the retired word ("harvested only"); fixer left it deliberately. One-word change ("reference lists mined only") when the file is next opened.

### R-024 — abilities.md "change shown" column: CLOSED
- `git diff 66351bd -- skills/screening/references/abilities.md`: line 3 now says the table carries no effect values and names where the pilot values (`change, delta, strength_sd, band` — all real evidence.csv columns) and the baselines live. No mention of an absent column.

### R-055 — population_sd.csv against the research document: CLOSED
- Diff shows only `n` (A07 blank→51), `source_doi` (4 added), `source_citation` (A07 "Sci Rep 2019 thermography (identify exact paper)" → "Gatt et al. 2019, Sci Rep 9:17204"), `population` (A04 "adults" → "young adults with typical hearing") and `notes` changed; mean/sd/unit identical. DOIs compared character by character with research-project.md refs 86–92: 10.3171/jns.1988.69.4.0552, 10.1038/s41598-019-53598-0, 10.5301/ejo.5001027, 10.1016/j.heares.2026.109547 all exact. Notes carry "551 measurements, 5 studies", "51 healthy controls, 510 finger readings", "91 normal eyes", "approximately 5; model estimate about 4", Wright URL, percentile derivations. All seven rows `pilot_unverified`.
- Executed: `Rscript -e 'read.csv("schema/population_sd.csv")'` → 7 × 12, n column parses (92457, NA, NA, 56, 51, 91, 126); `00_load.R` → "0 verified population-SD rows (of 7)".
- Undeclared change (not refuting): CHANGELOG says "Means, SDs, units unchanged" but does not say the A04 `population` cell changed; the new text matches document [92].

### R-057 — crosswalk to evidence.csv: CLOSED
- Python over the 26 table rows vs `INPUTS/data/evidence.csv`: 26 rows, `evidence_id` set == evidence.csv `id` set (one-to-one), bracketed feature == `feature` column for all 26, `key_sources` == `sources` column verbatim for all 26, problems: []. The mapping rationale and the reviewer's paraphrase examples (A01, A03) are stated in line 5; exclusions line matches.

### R-068 — DRAFT Outcome criterion vs charter D2: PARTIAL (builder part done; row owned by Sean)
- Read: `screening/SKILL.md:32` Outcome bullet admits "a validated rating instrument for pain (intensity, unpleasantness) or a seizure diary/count"; "unvalidated self-report alone is not an outcome"; labelled "Aligned to charter D2 … research document's scope ('measured objectively or by a validated rating'); confirm at G2 (R-068)". E3 (line 40) reworded to match. Quote checked against `research-project.md:17` ("measured objectively or by a validated rating") — exact. Under this text Zeidan 2011 (validated pain ratings) is no longer E3; A10, A11, A13 stay. This is exactly the contract's R-068 exception. The scope ruling remains Sean's; OPEN_DECISIONS.md:35 carries it.

### R-073 — exclusion-code order and E6: CLOSED
- Read: rule 3 tests E7 first and stops; then E1–E5 in numeric order; E8 only for unobtainable full text; code list re-ordered E7, E1–E5, E8; E6 moved to a head-agent paragraph (`screener_id = head-agent`), rule 7 extended ("You never judge whether a record duplicates another one"); SCHEMA.md:54-55 states the same order and E6 ownership; Output line 16 lists the screener codes without E6. Matches contract item 7 verbatim. Walk-through: a narrative overview (E4 would apply) and a meta-analysis (E3 would apply) both stop at E7.
- Note: SCHEMA adds `head-agent` to the `screener_id` vocabulary; no code validates `screener_id`, so nothing breaks.

## Contract items 1–3, 6, 7 (no register id) — checked
- Item 1: SCHEMA.md master table has `pre_post_r` and `is_primary_outcome` rows with the contract's meaning; header already carried them after `n_tested` (unchanged). Extraction skill lines 17–19 tell extractors to leave `is_primary_outcome` blank.
- Item 2/3: SCHEMA §Effect-size conventions lists the 15 effect_sizes.csv columns and SMD/SMCR/PLO/OR/Z exactly as in the contract; SE→SD and CI95→SD formulas present; r = 0.5 labelled "placeholder pending the statistician co-author's decision at Gate 5" in SCHEMA:107 and extraction SKILL:18.
- Item 6, 7: verified above (R-013, R-022, R-073).
- Item 9: CHANGELOG_C.md has one line per id in the `R-0xx | files | what | how verified` form and a Not-closed list; no commit.
- Item 11: nothing contacted, scheduled or posted by fixer or verifier.

## Contract violations / deviations
1. **Documentation contradicts executed behaviour** (C-owned): RECONCILIATION.md:35 and SCHEMA.md:102 claim 00_load.R only warns on a blank `is_primary_outcome`; it refuses the file (executed, see R-019). Fix the two sentences ("the loader refuses blank values; set `--primary` before loading").
2. **Sean-owned row text changed**: `skills/screening/SKILL.md:48` (R-021's subject, "Sean or a co-author") was rewritten to "the two human co-authors … Sean adjudicates and does not code". The contract says Sean-owned rows' files are left as they are; OPEN_DECISIONS.md:20 records it as "changed in this round to match the charter — Confirm", so it is disclosed, not hidden. Flagged for Sean's confirmation.
3. Minor: appraisal SKILL.md:15 retains "harvested only"; SCHEMA.md:3 "seven" miscount; CHANGELOG omits the A04 `population` change.

## Files outside ownership
None attributable to fixer C. All other working-tree changes (analysis/**, dry-run/**, reporting/**, monitor/**, traces/trace_logger.py, TRACE_SPEC.md, test_trace_logger.py, CHANGELOG_A/B/D, OPEN_DECISIONS.md, VERIFY_A.md, analysis/outputs/* untracked outputs) belong to fixers A, B, D, the head agent or other verifiers. `traces/stage1.jsonl` gained C's record through the logger only.
Verifier footprint: created `traces/prompts/verify_C_2026-10-04.md`, this file, and the two trace lines (start/end) via `flock traces/.lock`; my loader run wrote `analysis/outputs/REFUSED_vocabulary.csv` inside the package, which I deleted again (mtime confirmed it was mine). Scratch work in `scratchpad/verify_C_test`, `verify_C_test2`, `verify_C_sof` (outside the package).

## Cross-area observations (not C's to fix)
- B's `analysis/synthetic/grade_final_synthetic.csv` uses `final_certainty = moderate` (lowercase); SCHEMA.md (C) specifies `High`, `Moderate`, `Low`, `Very low`. One of the two should move.
- `dry-run/DRY_RUN_PROTOCOL.md:33` (D) now reads E7/exclude for Paravlic 2018 — consistent with C's screening skill.

## Judgment
Fixer C: 8 closed (R-013, R-014, R-019, R-022, R-024, R-055, R-057, R-073), 2 partial as declared (R-020 skill part done, κ and "who codes" are Sean's; R-068 redraft done, ruling is Sean's), 0 not closed, 0 regressed; every claimed test reproduced; one false sentence about loader behaviour in RECONCILIATION.md/SCHEMA.md must be corrected before the dry run; no file outside C's ownership touched.

## Appendix — `git status --porcelain` (whole tree, 2026-10-04 12:29Z)
```
 M analysis/00_load.R
 D analysis/01_frequentist.R
 D analysis/02_bayesian.R
 D analysis/03_sof.R
 M analysis/ENVIRONMENT.md
 M analysis/run_all.R
 M analysis/setup.R
 M dry-run/DRY_RUN_PROTOCOL.md
 M monitor/MONITOR_SPEC.md
 M reporting/METHODS_PAPER_OUTCOMES.md
 M reporting/REPORTING_PLAN.md
 M schema/SCHEMA.md
 M schema/population_sd.csv
 M skills/appraisal/SKILL.md
 M skills/extraction/SKILL.md
 M skills/screening/SKILL.md
 M skills/screening/references/abilities.md
 M traces/TRACE_SPEC.md
 M traces/stage1.jsonl
 M traces/trace_logger.py
?? CHANGELOG_A.md  CHANGELOG_B.md  CHANGELOG_C.md  CHANGELOG_D.md  OPEN_DECISIONS.md  VERIFY_A.md
?? analysis/01_effect_sizes.R  analysis/02_frequentist.R  analysis/03_bayesian.R  analysis/04_sof.R  analysis/constants.R  analysis/synthetic/  analysis/outputs/*
?? dry-run/decoys.csv  dry-run/selection.csv  reporting/templates/
?? schema/grade_draft.csv  schema/grade_final.csv  tools/
?? traces/prompts/build_run_2026-10-04_RETROACTIVE.md  traces/prompts/fix_{A,B,C,D}_2026-10-04.md  traces/prompts/verify_{A,B,C}_2026-10-04.md  traces/test_trace_logger.py
```
