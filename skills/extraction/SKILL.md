---
name: vcr-extraction
description: Field-by-field data extraction with a mandatory provenance block for the voluntary-control systematic review, applied as one of two independent extractors. Use this skill whenever you are asked to extract effects, means, SDs, sample sizes, prevalence counts or study characteristics from an included paper into master_extraction.csv, even if the request just says "pull the numbers from this paper".
---

# Extraction skill (one of two independent extractors)

You are extractor A or extractor B. You never read the other extractor's rows. The head agent diffs the two files with tools/reconcile.py (procedure in tools/RECONCILIATION.md); Sean adjudicates every discrepancy in adjudication_log.csv; the statistician co-author spot-checks; the reconciled file extraction/master_reconciled.csv is the only file the analysis code reads.

## Inputs
- study_id and the full text (PDF or HTML path under extraction/fulltext/). Supplementary files if present.
- The ability_id(s) this study informs (skills/screening/references/abilities.md).

## Output
Rows in schema/master_extraction.csv — one row per outcome × condition × timepoint. Field definitions and allowed values are in schema/SCHEMA.md. No row is valid without every provenance field filled.

Two fields are handled differently from the rest:
- `pre_post_r`: for within-person designs (`pre_post`, `crossover`), the correlation between the pre and post measurements. Record it only when it is printed, or when it is derivable from printed numbers (then `derivation` states the formula and inputs, e.g. from the SD of the change and the two SDs). Otherwise leave it blank and say so in `notes` ("pre/post correlation not reported"); the analysis code then uses the placeholder r = 0.5 (pending the statistician co-author's decision at Gate 5) and runs sensitivity at 0.3 and 0.7. Never guess it.
- `is_primary_outcome`: leave blank. The head agent sets it (`yes`/`no`, one primary outcome per study × ability) at reconciliation with `tools/reconcile.py build --primary`; extractors do not decide which outcome is primary.

## Rules
1. Enter numbers exactly as printed, in the printed unit. Unit conversion, SD-from-SE, SD-from-CI, change-from-pre-post and effect-size computation are done in analysis code (analysis/01_effect_sizes.R), not by you. If you must record a derived number, put the formula and inputs in `derivation` and set `value_source = derived`.
2. Dispersion as printed, typed: if the paper gives an SD, `dispersion_type = SD` and `dispersion_value` = the SD; if it gives an SE, `dispersion_type = SE` and `dispersion_value` = the SE (do not multiply by √n); if it gives a 95% CI, `dispersion_type = CI95`, `ci_low` and `ci_high` as printed, `dispersion_value` blank. The code converts with sd = se·√n and sd = (hi − lo)/(2·1.96)·√n and records the derivation, so `n_condition` must be on the same row. An interval at another level (90%, 99%), an IQR or a range is recorded with its own type (`IQR`, `range`) or, for a non-95% interval, with the bounds in `ci_low`/`ci_high`, `dispersion_type = none` and the level stated in `notes`; never rescale it to a 95% interval yourself.
3. Values read from a figure get `value_source = figure` and a precision note ("read to ±0.1 °C from Fig 2B"). Values from supplements get `value_source = supplement` with the file name.
4. `verbatim_anchor` is up to 20 words copied exactly from the source at the location, so the reviewer can find the number. It is a locator, not a quotation for the manuscript.
5. Missing is blank, with the reason in `notes` ("SD not reported; only SE"). Never impute, estimate or infer a number that is not printed.
6. `verification_route` states how you saw the source: `pdf_full_text`, `html_full_text`, `supplement`, `abstract_only`, `not_opened`. Rows with `abstract_only` or `not_opened` are provisional and are flagged for Sean.
7. Record the comparator on its own row (same outcome, `condition_label = control` or `baseline`). Record n per condition, not just total n. For within-person designs, the pre value may instead sit in `baseline_value`/`baseline_dispersion` on the same row when the paper reports change from baseline.
8. Case reports: one row per measured episode, n_condition = 1. Prevalence surveys: `n_responders` and `n_tested` with the exact question or test used in `outcome_measure`.
9. Record the lever: `feedback`, `breathing`, `muscle`, `imagery`, `suggestion`, `none`, `mixed`, `unclear`. This is a pre-specified subgroup.
10. Population-SD sources (resting values in healthy adults used for the z scale) go to schema/population_sd.csv, not to the master file.
11. Immune-challenge or endotoxin studies (A09): do not extract in a background agent. Return the study to the head agent for main-session extraction with Sean present.
12. Do not assess risk of bias here; that is the appraisal skill. Do not search for other papers.
13. Write the key fields (`study_id`, `ability_id`, `outcome_measure`, `condition_label`, `timepoint`) consistently across your rows and with the study's screening record, because the reconciliation diff matches rows on exactly these five fields; a spelling difference there is reported as a missing row, not as a field discrepancy.
14. Log the run with traces/trace_logger.py before and after (role `extraction`, instance A or B).

## Blind human subset (charter D4)
After full-text screening closes, the head agent draws a seeded random 10–20% subset of the included studies (seed recorded in the trace). The two human co-authors (the statistician co-author and the subject-matter co-author; charter D4), dividing the subset between them, extract each subset study into the same schema/master_extraction.csv layout with `extractor_id = human-<initials>`, blind to both agent files; Sean adjudicates and therefore does not extract. The head agent then runs `tools/reconcile.py diff` of the human file against the reconciled agent file and computes the field-level exact-agreement rate and the numeric discrepancy rate (agent vs human), which feed reporting/METHODS_PAPER_OUTCOMES.md #4 alongside the agent–agent figures. You are not told which studies are in the subset, and the human rows never enter master_reconciled.csv unless Sean's adjudication log says so.

## Dry-run check
On a dry-run study, after filling your rows, do not look up the expected number. Report what you extracted; the head agent compares it with the research document's verified value.
