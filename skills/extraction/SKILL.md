---
name: vcr-extraction
description: Field-by-field data extraction with a mandatory provenance block for the voluntary-control systematic review, applied as one of two independent extractors. Use this skill whenever you are asked to extract effects, means, SDs, sample sizes, prevalence counts or study characteristics from an included paper into master_extraction.csv, even if the request just says "pull the numbers from this paper".
---

# Extraction skill (one of two independent extractors)

You are extractor A or extractor B. You never read the other extractor's rows. The head agent diffs the two files; Sean adjudicates conflicts; the statistician co-author spot-checks.

## Inputs
- study_id and the full text (PDF or HTML path under extraction/fulltext/). Supplementary files if present.
- The ability_id(s) this study informs (skills/screening/references/abilities.md).

## Output
Rows in schema/master_extraction.csv — one row per outcome × condition × timepoint. Field definitions and allowed values are in schema/SCHEMA.md. No row is valid without every provenance field filled.

## Rules
1. Enter numbers exactly as printed, in the printed unit. Unit conversion, SD-from-SE, change-from-pre-post and effect-size computation are done in analysis code, not by you. If you must record a derived number, put the formula and inputs in `derivation` and set `value_source = derived`.
2. Values read from a figure get `value_source = figure` and a precision note ("read to ±0.1 °C from Fig 2B"). Values from supplements get `value_source = supplement` with the file name.
3. `verbatim_anchor` is up to 20 words copied exactly from the source at the location, so the reviewer can find the number. It is a locator, not a quotation for the manuscript.
4. Missing is blank, with the reason in `notes` ("SD not reported; only SE"). Never impute, estimate or infer a number that is not printed.
5. `verification_route` states how you saw the source: `pdf_full_text`, `html_full_text`, `supplement`, `abstract_only`, `not_opened`. Rows with `abstract_only` or `not_opened` are provisional and are flagged for Sean.
6. Record the comparator on its own row (same outcome, `condition_label = control` or `baseline`). Record n per condition, not just total n.
7. Case reports: one row per measured episode, n_condition = 1. Prevalence surveys: `n_responders` and `n_tested` with the exact question or test used in `outcome_measure`.
8. Record the lever: `feedback`, `breathing`, `muscle`, `imagery`, `suggestion`, `none`, `mixed`, `unclear`. This is a pre-specified subgroup.
9. Population-SD sources (resting values in healthy adults used for the z scale) go to schema/population_sd.csv, not to the master file.
10. Immune-challenge or endotoxin studies (A09): do not extract in a background agent. Return the study to the head agent for main-session extraction with Sean present.
11. Do not assess risk of bias here; that is the appraisal skill. Do not search for other papers.
12. Log the run with traces/trace_logger.py before and after (role `extraction`, instance A or B).

## Dry-run check
On a dry-run study, after filling your rows, do not look up the expected number. Report what you extracted; the head agent compares it with the research document's verified value.
