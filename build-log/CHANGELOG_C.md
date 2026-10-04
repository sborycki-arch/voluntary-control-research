# CHANGELOG_C — fixer C (skills and schema), round-2 build, 2026-10-04

Trace of this run: `s1-builder-C-20261004T120715Z-fd60` (prompt `traces/prompts/fix_C_2026-10-04.md`). Files owned and touched: `schema/SCHEMA.md` (rewritten), `schema/population_sd.csv`, `schema/grade_draft.csv` (new), `schema/grade_final.csv` (new), `skills/screening/SKILL.md`, `skills/screening/references/abilities.md`, `skills/extraction/SKILL.md`, `skills/appraisal/SKILL.md` (two lines only), `tools/reconcile.py` (new), `tools/RECONCILIATION.md` (new), this file. `schema/screening_decisions.csv`, `schema/appraisal.csv` and `schema/master_extraction.csv` headers were checked and left unchanged (the master header already carried `pre_post_r`, `is_primary_outcome` after `n_tested`). Nothing committed.

## Register rows

R-013 | schema/SCHEMA.md, schema/grade_draft.csv, schema/grade_final.csv, skills/appraisal/SKILL.md | SCHEMA.md gains grade_draft.csv (21 columns, contract item 6) and grade_final.csv (same 21 + final_certainty, final_rater_id, final_date, change_reason, signed) sections with field meanings; `outcome` is defined as the primary row's `outcome_measure` string so 04_sof.R joins on ability_id + outcome; header-only templates created in schema/; live-file locations (reporting/) stated. | `cat schema/grade_draft.csv schema/grade_final.csv` → headers byte-identical to contract item 6; python check `grade_final = draft + 5: True`; the header matches the columns 04_sof.R reads (`grade_cols` in analysis/04_sof.R:16) and analysis/synthetic/grade_final_synthetic.csv (B's file, same 26 columns). CLOSED.

R-014 | skills/appraisal/SKILL.md | Output field list now reads the 12 appraisal.csv fields including `notes`; no other line of the file changed (R-044, R-045, R-071 untouched). | `git diff --stat skills/appraisal/SKILL.md` → 2 insertions, 2 deletions; python check `appraisal fields identical: True` (list parsed from the skill == schema/appraisal.csv header). CLOSED.

R-019 | tools/reconcile.py, tools/RECONCILIATION.md, schema/SCHEMA.md, skills/extraction/SKILL.md | Reconciliation defined end to end: `reconcile.py diff` keyed on study_id, ability_id, outcome_measure, condition_label, timepoint writes discrepancies.csv (discrepancy_id, key, field, value_A, value_B, type ∈ missing_in_A, missing_in_B, numeric, text, provenance); `reconcile.py build` applies adjudication_log.csv (discrepancy_id, decision A/B/other, chosen_value, adjudicator, date, reason), refuses while any discrepancy lacks a log row (also on stale ids and malformed rows), sets is_primary_outcome from `--primary` or leaves blank with a warning, writes master_reconciled.csv for 00_load.R. RECONCILIATION.md gives the procedure, roles, log schema, what is compared, the human-subset comparison and how the result feeds 00_load.R; SCHEMA.md has a Reconciliation-files section. Run-metadata fields (extractor_id, extraction_date, skill_version, model) are not diffed (they always differ between runs) and are rewritten on reconciled rows (`extractor_id = reconciled`, added to the SCHEMA vocabulary). | Test on two synthetic files (scratchpad/reconcile_test, outside the package), transcript below: diff → 9 discrepancies covering all five types; empty log → exit 2, nothing written; partial log (8/9) → exit 2 naming D-0009; malformed log → exit 2 with 5 named problems; full log without --primary → exit 0 plus warning, blank column; with --primary → exit 0, yes/no set, 2 warnings; duplicate key → exit 2; `Rscript analysis/00_load.R` (scratch copy, VCR_MASTER = the built file) → "Loaded 5 rows, 2 abilities", exit 0. CLOSED.

R-020 (extraction-skill part) | skills/extraction/SKILL.md, tools/RECONCILIATION.md | New section "Blind human subset (charter D4)": head agent draws a seeded 10–20% subset of included studies (seed in trace); a human co-author (statistician or subject-matter co-author) extracts into the same schema with extractor_id human-<initials>, blind to agent output; Sean adjudicates and does not extract; head agent runs `reconcile.py diff` human vs reconciled and computes field-level agreement and numeric discrepancy rate, feeding METHODS_PAPER_OUTCOMES #4. | Read-through against charter D4 text ("code the blind 10–20% human subset that gives screening and extraction agent-vs-human κ"); the diff mechanism it relies on was executed (R-019 transcript). CLOSED for the skill part; the METHODS_PAPER_OUTCOMES #4 wording is fixer D's (contract table).

R-022 | skills/screening/SKILL.md, schema/SCHEMA.md | Harvest coding fixed: a review/meta-analysis/overview is `decision = exclude`, `exclusion_code = E7`; `harvest` removed as a code value from the skill (rule 6, DRAFT design bullet, code list) and from SCHEMA (exclusion_code vocabulary now E1–E8 or blank; PRISMA-flow and κ consequences stated). | `grep -rn -i harvest skills schema tools` → three prose mentions only (screening rule 6 and SCHEMA both say it is not a code value; appraisal SKILL.md:15 "harvested only" is prose in a file I was told to change nothing else in). CLOSED.

R-024 | skills/screening/references/abilities.md | Line 3 rewritten: the table carries no effect values; pilot values live in INPUTS/data/evidence.csv and the research document's evidence sections (rationale only, charter SC1); population baselines live in schema/population_sd.csv. | Read-through; the file no longer mentions a "change shown" column. CLOSED.

R-055 | schema/population_sd.csv | DOIs added for Uematsu (10.3171/jns.1988.69.4.0552), Gatt (10.1038/s41598-019-53598-0), Schröder (10.5301/ejo.5001027), Shahnaz & Ciocca (10.1016/j.heares.2026.109547); "Sci Rep 2019 thermography (identify exact paper)" replaced by "Gatt et al. 2019, Sci Rep 9:17204", n = 51, notes "51 healthy controls, 510 finger readings"; hearing SD kept 5.0 with notes "document [92]: approximately 5; model estimate about 4"; Geneva notes "551 measurements, 5 studies" (n left blank, measurements not persons); Schröder notes "91 normal eyes"; Wright URL in notes (no source_url column; also the two percentile derivations from the document); Quer and Uematsu sample descriptors carried. Means, SDs, units unchanged; every row `pilot_unverified`. | Values copied from research-project.md lines 46–55 and references 86–92 and INPUTS/data/baselines.csv (read in this run); `Rscript analysis/00_load.R` in the scratch copy read the file: "0 verified population-SD rows (of 7)", so nothing enters analysis. CLOSED.

R-057 | skills/screening/references/abilities.md | Columns `evidence_id` (evidence.csv `id`, with the evidence-map `feature` name in brackets) and `key_sources` (evidence.csv `sources`, verbatim) added to all 26 rows; the one-to-one mapping by name is stated in the file, with the paraphrase examples the reviewer gave; exclusions line notes evidence.csv carries the same two. | Generated by script from INPUTS/data/evidence.csv with assertions: 26 mapping entries, set of mapped ids == set of evidence.csv ids, 26 table rows written, no `|` inside copied cells. CLOSED.

R-068 | skills/screening/SKILL.md | DRAFT Outcome bullet now: "an instrumented physiological measurement, or a validated rating instrument for pain (intensity, unpleasantness) or a seizure diary/count; unvalidated self-report alone is not an outcome", with the prevalence clause kept and the line "Aligned to charter D2 … and the research document's scope ('measured objectively or by a validated rating'); confirm at G2 (R-068)". E3 reworded to "no admissible measurement: neither an instrumented physiological measurement nor a validated rating instrument for pain or a seizure diary/count (unvalidated self-report or observer impression only)". A10, A11, A13 and the dry-run candidate Zeidan 2011 are no longer excluded at screening by the draft text. | Read-through against charter D2 (pain, seizure frequency named) and research-project.md:17. Redraft done as the contract's R-068 exception; the scope ruling stays Sean's. PARTIAL (builder part done; "confirm at G2" is Sean's).

R-073 | skills/screening/SKILL.md | Rule 3 now tests E7 first and stops; then E1–E5 in numeric order; E8 only for unobtainable full text. Code list re-ordered E7, E1–E5, E8. E6 moved out of the screener list into a head-agent deduplication note (screener_id head-agent; screeners never apply it); rule 7 extended ("you never judge whether a record duplicates another one"). SCHEMA states the test order and the E6 ownership. | Read-through: a narrative overview (E4 would apply) and a meta-analysis (E3 would apply) now stop at E7 before E3/E4 are reached; no screener rule requires knowledge of other records. CLOSED.

Also done (contract items 1–3, 6, 7, no register id): SCHEMA.md master table gains `pre_post_r` and `is_primary_outcome` rows (meaning, who sets them, placeholder r = 0.5 pending the statistician co-author's decision at Gate 5), key-field statement, `reconciled` extractor_id and merged skill_version/model forms; Effect-size conventions rewritten to SMD/SMCR/PLO/OR/Z with the SE→SD and CI95→SD formulas, `synthetic` flag, pooling unit ability_id × measure on primary rows, k ≥ 3, dependent-effect-size note (multilevel = Gate 5), Bayesian routing note. Extraction skill gains the two-field paragraph (extractors leave is_primary_outcome blank; pre_post_r only when printed or derivable), rule 2 on recording SE/CI95/other intervals as printed with n_condition on the row (conversions in code), rule 13 on key-field consistency, and the reconcile.py pointer.

## Test transcript for tools/reconcile.py (synthetic files in scratchpad/reconcile_test, not in the package)

Synthetic A.csv (5 rows) and B.csv (5 rows) in the master_extraction.csv layout; differences planted: a row only in A, a row only in B, `value` 27.0 vs 27.2, `location` differing, `instrument` blank in A, `pre_post_r` 0.6 vs 0.65, `instrument` and `p_value` blank in B, `notes` text differing, and `value` 5 vs 5.0 (numerically equal, expected not to be reported).

```
$ python3 tools/reconcile.py diff A.csv B.csv --out discrepancies.csv
reconcile diff: 5 rows in A, 5 in B, 4 keys in common, 9 discrepancies -> discrepancies.csv
  missing_in_A  2
  missing_in_B  3
  numeric       2
  text          1
  provenance    1
exit 0

discrepancy_id,key,field,value_A,value_B,type
D-0001,synth_only_in_A_2019|A03|axillary temperature|intervention|end of training,row,row present,,missing_in_B
D-0002,synth_only_in_B_2021|A21|can move one ear|survey|single,row,,row present,missing_in_A
D-0003,synth_test_2020|A07|finger skin temperature|baseline|end of training,value,27.0,27.2,numeric
D-0004,synth_test_2020|A07|finger skin temperature|baseline|end of training,location,"p. 3, Table 1, row 1","p. 3, Table 1",provenance
D-0005,synth_test_2020|A07|finger skin temperature|intervention|end of training,instrument,,thermistor,missing_in_A
D-0006,synth_test_2020|A07|hand temperature|intervention|session 1,pre_post_r,0.6,0.65,numeric
D-0007,synth_test_2020|A07|skin conductance|intervention|t1,instrument,thermistor,,missing_in_B
D-0008,synth_test_2020|A07|skin conductance|intervention|t1,p_value,0.03,,missing_in_B
D-0009,synth_test_2020|A07|skin conductance|intervention|t1,notes,SE as printed,standard error,text

$ python3 tools/reconcile.py build A.csv B.csv log_empty.csv --out master_reconciled.csv     # header-only log
reconcile: discrepancy D-0001 has no adjudication-log row (synth_only_in_A_2019|A03|axillary temperature|intervention|end of training; field row; A='row present'; B=''; type missing_in_B)
... (one line per discrepancy, D-0001 to D-0009) ...
reconcile: refusing to build: 9 of 9 discrepancies are not adjudicated
exit 2
ls: cannot access 'master_reconciled.csv': No such file or directory

$ python3 tools/reconcile.py build A.csv B.csv log_partial.csv --out master_reconciled.csv   # 8 of 9 rows logged
reconcile: discrepancy D-0009 has no adjudication-log row (synth_test_2020|A07|skin conductance|intervention|t1; field notes; A='SE as printed'; B='standard error'; type text)
reconcile: refusing to build: 1 of 9 discrepancies are not adjudicated
exit 2

$ python3 tools/reconcile.py build A.csv B.csv log_bad.csv --out master_reconciled.csv       # stale id, decision C, other without chosen_value, row discrepancy with other, blank reason
reconcile: adjudication log line 3 (D-0002): a whole-row discrepancy takes decision A or B, not other
reconcile: adjudication log line 3 (D-0002): reason is blank
reconcile: adjudication log line 4 (D-0003): decision other needs a chosen_value
reconcile: adjudication log line 7 (D-0006): decision must be A, B or other, got 'C'
reconcile: adjudication log line 11: D-0099 is not a discrepancy of these two files (stale or wrong log)
exit 2

$ python3 tools/reconcile.py build A.csv B.csv log_full.csv --out master_noprimary.csv --date 2026-10-04
reconcile: warning: no --primary file given: is_primary_outcome left blank on every row; nothing will enter pooling until it is set
reconcile build: 9 discrepancies applied from log_full.csv; 5 row(s) written, 1 row(s) dropped by adjudication -> master_noprimary.csv
exit 0

$ python3 tools/reconcile.py build A.csv B.csv log_full.csv --primary primary.csv --out master_reconciled.csv --date 2026-10-04
reconcile: warning: study synth_only_in_A_2019 x ability A03 has no is_primary_outcome = yes row (no matching primary-outcome entry)
reconcile: warning: primary-outcome entry synth_nowhere_2000 x A01 ('heart rate') matches no reconciled row
reconcile build: 9 discrepancies applied from log_full.csv; 5 row(s) written, 1 row(s) dropped by adjudication -> master_reconciled.csv
exit 0
# result: D-0003 other → value 27.1; D-0006 B → pre_post_r 0.65; D-0009 other → merged notes; D-0002 A → B-only row dropped;
# D-0001 A → A-only row kept with its own skill_version/model; extractor_id = reconciled on every row; is_primary_outcome yes on the
# two "finger skin temperature" rows of synth_test_2020, no elsewhere.

$ python3 tools/reconcile.py diff A_dup.csv B.csv --out x.csv                                 # A with a duplicated key
reconcile: A: duplicate key on line 7 (first seen line 6): synth_test_2020|A07|skin conductance|intervention|t1
reconcile: A: key fields (study_id, ability_id, outcome_measure, condition_label, timepoint) must be unique within one extractor file
exit 2

$ VCR_MASTER=.../reconcile_test/master_reconciled.csv Rscript analysis/00_load.R              # scratch copy of analysis/ + schema/
Warning message:
1 study x ability combination(s) have no is_primary_outcome = yes row (synth_only_in_A_2019 A03); they will not enter pooling
Loaded 5 rows, 2 abilities from .../reconcile_test/master_reconciled.csv; 0 verified population-SD rows (of 7) from schema/population_sd.csv
exit 0
```

Other checks run: `python3 -m py_compile tools/reconcile.py` → compiled; frontmatter check on all four SKILL.md files → each has non-empty `name` and `description` (vcr-appraisal, vcr-extraction, vcr-reviewer, vcr-screening); `git status --short -- skills schema tools` → only the files listed at the top.

## Not closed
- R-068: the redraft is in place and labelled "confirm at G2 (R-068)"; whether validated ratings are admissible (and so whether A10, A11, A13 stay in the review) is Sean's scope ruling. The row stays open for Sean on that point.
- R-020: the extraction-skill part is done; METHODS_PAPER_OUTCOMES.md #4 (agent-vs-human extraction κ / agreement wording) is in fixer D's scope and the charter question "is extraction κ required?" is Sean's.
- Outside my ownership but affected by R-022/R-073: dry-run/DRY_RUN_PROTOCOL.md still says "harvest only" for Paravlic 2018 (fixer D's file); skills/appraisal/SKILL.md:15 says "(harvested only)" as prose — left because the instruction was to change nothing else in that file; it is not a code value.
- reconcile.py design choice to flag: extractor_id, extraction_date, skill_version and model are not diffed (they always differ between two runs and would force one no-information log row per row). If the coordinator wants them listed as `provenance` discrepancies anyway, it is a one-line change to RUN_METADATA_FIELDS.

## Open questions for Sean
1. R-068: confirm at G2 that validated pain ratings (intensity, unpleasantness) and seizure diaries/counts are admissible outcomes for A10, A11, A13, as the redrafted criterion now says; otherwise the three abilities leave the review and the criterion reverts.
2. Primary-outcome hierarchy: `reconcile.py build --primary` needs one primary outcome per study × ability from a pre-specified hierarchy; the hierarchy itself is not written anywhere yet (protocol, Gate 2). Who drafts it, and before which gate?
3. The log's `reason` vocabulary for methods-paper outcome #4 (misread, wrong row, unit, omission, source ambiguity, other) is proposed in tools/RECONCILIATION.md; confirm or amend before the dry run so the discrepancy-by-type count is fixed in advance.
