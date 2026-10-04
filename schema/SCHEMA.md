# Schema dictionary

All CSV files in this package are UTF-8, comma-separated, header row as given, blank cell = missing. This file defines nine of them: master_extraction.csv, screening_decisions.csv, appraisal.csv, population_sd.csv, grade_draft.csv, grade_final.csv (header templates in schema/; live files are written where each section says) and the reconciliation files (discrepancies.csv, adjudication_log.csv, master_reconciled.csv; layout here, procedure in tools/RECONCILIATION.md). The analysis code (analysis/00_load.R) refuses any master row whose provenance fields (source_doi or source_url, location, verbatim_anchor, extractor_id, extraction_date, verification_route) are empty, whose skill_version or model is blank, or whose controlled-vocabulary values are outside the lists below.

## master_extraction.csv — one row per outcome × condition × timepoint
Header template: schema/master_extraction.csv. Extractor files are written to extraction/<study or batch>_A.csv and _B.csv; the analysis reads only extraction/master_reconciled.csv (see Reconciliation).

| Field | Meaning / allowed values |
|---|---|
| study_id | `firstauthor_year` plus a letter if needed (`benson_1982a`); `synth_` prefix marks synthetic test data |
| record_id | id from the records file |
| ability_id | A01–A26 (skills/screening/references/abilities.md); semicolon-separated if a row informs more than one |
| design | `rct`, `crossover`, `nonrandomised_comparison`, `pre_post`, `case_report`, `case_series`, `prevalence_survey`, `other` (state in notes) |
| population | free text as printed (age, health status, expertise) |
| n_total | total analysed in the study |
| condition_label | `intervention`, `control`, `baseline`, `sham`, or the printed label; never blank |
| n_condition | n analysed in this condition (needed for every SE or CI conversion) |
| comparator_label | `condition_label` of the row this one is compared with, blank if none; the code pairs rows on study_id + outcome_measure + timepoint + this label |
| lever_type | `feedback`, `breathing`, `muscle`, `imagery`, `suggestion`, `none`, `mixed`, `unclear` |
| outcome_measure | what was measured, as printed (`hearing threshold at 250 Hz`); the same string on every row of that outcome, because it is a key field |
| instrument | device or method (`tympanometry`, `infrared thermistor`) |
| unit | as printed |
| timepoint | as printed (`end of 12 weeks`, `during contraction`) |
| stat_type | `mean`, `median`, `mean_change`, `percent`, `count`, `max_individual`, `other` |
| value | the number as printed |
| dispersion_type | `SD`, `SE`, `CI95`, `IQR`, `range`, `none` |
| dispersion_value | SD, SE or IQR width as printed, never converted; for CI95 use ci_low and ci_high and leave this blank |
| ci_low, ci_high | as printed |
| p_value | as printed (`<0.001`, `0.03`) |
| baseline_value, baseline_dispersion | pre-intervention values on the same row when the paper reports change from baseline (within-person designs) |
| n_responders, n_tested | prevalence designs and binary outcomes: numerator and denominator |
| pre_post_r | within-person designs (`pre_post`, `crossover`): correlation between the pre and post measurements, as printed or derivable from printed numbers (derivation stated); numeric in [−1, 1]; blank if not reported. Blank rows get the placeholder r = 0.5 in analysis (see Effect-size conventions). Recorded by extractors, never estimated |
| is_primary_outcome | `yes`/`no`; exactly one primary outcome (one `outcome_measure` string, all its rows flagged `yes`) per study × ability. Extractors leave it blank; the head agent sets it at reconciliation from the primary-outcome file (`tools/reconcile.py build --primary`), following the pre-specified outcome hierarchy agreed for the protocol. Only `yes` rows enter pooling |
| value_source | `text`, `table`, `figure`, `supplement`, `derived` |
| derivation | formula and inputs if `derived` (also for a derived pre_post_r) |
| source_doi, source_url | at least one required |
| location | page, table, figure or section (`p. 1236, Table 2, row 3`) |
| verbatim_anchor | ≤ 20 words copied exactly from the location |
| extractor_id | `agent-extraction-A`, `agent-extraction-B`, `human-<initials>`; `reconciled` in master_reconciled.csv (written by tools/reconcile.py) |
| extraction_date | ISO date |
| verification_route | `pdf_full_text`, `html_full_text`, `supplement`, `abstract_only`, `not_opened` (the last two are provisional and stop the analysis) |
| skill_version | git short hash of skills/extraction at run time; in master_reconciled.csv `A=<hash>;B=<hash>` when the two runs differ |
| model | exact model string from the run; in master_reconciled.csv `A=<string>;B=<string>` when the two runs differ |
| notes | free text; reasons for blanks |

Key fields: `study_id`, `ability_id`, `outcome_measure`, `condition_label`, `timepoint` identify a row and must be unique within one extractor file; the reconciliation diff matches rows on them.

## screening_decisions.csv
Header template: schema/screening_decisions.csv; live file screening/screening_decisions.csv.
record_id · stage (`ta`, `ft`) · decision (`include`, `exclude`, `unsure`) · exclusion_code (`E1`, `E2`, `E3`, `E4`, `E5`, `E6`, `E7`, `E8` or blank; no other value) · rationale (≤ 40 words with a quoted phrase) · confidence (`high`, `medium`, `low`) · screener_id (`agent-screening-A`, `agent-screening-B`, `human-<initials>`, `head-agent` for E6 only) · skill_version · model · timestamp (ISO 8601).

Coding conventions (skills/screening/SKILL.md):
- A review, meta-analysis or overview is `decision = exclude`, `exclusion_code = E7`. There is no `harvest` code value; reference-list mining of E7 records is a Stage 3 head-agent step. PRISMA flow: E7 records count as excluded at the stage where they were coded, and the mined references enter the flow as "records identified from citation searching".
- Codes are tested in the order E7, E1, E2, E3, E4, E5; E8 (full text not obtainable) always pairs with `decision = unsure`.
- E6 (duplicate) is written only by the head agent during deduplication (`screener_id = head-agent`); screener rows never carry it.
- Agreement statistics (κ) are computed on `decision` and, among excludes, on `exclusion_code`.

## appraisal.csv
Header template: schema/appraisal.csv; live file appraisal/appraisal.csv.
study_id · tool (`rob2`, `rob2_crossover`, `robins_i`, `jbi_case_report`, `jbi_case_series`, `jbi_prevalence`) · tool_version (date or version string) · domain (tool's domain or item name, or `overall`) · judgment (tool vocabulary; see skills/appraisal/SKILL.md) · rationale · source_location · rater_id (`agent-appraisal`, `agent-appraisal-A`, `agent-appraisal-B`, `human-<initials>`) · date · skill_version · model · notes (tool-selection rule used, and anything else).

## population_sd.csv
Resting-value sources for the Z scale (schema/population_sd.csv, read directly by 00_load.R).
ability_id (A-codes, semicolon-separated when shared) · variable · mean · sd · unit (matched case-insensitively to the master row's `unit`) · population · n (persons; blank when the source counts measurements or eyes, stated in notes) · source_doi · source_citation · location · status (`pilot_unverified` until a dual-extracted row with provenance replaces it; `verified` thereafter) · notes (sample descriptors from the research document, URL when there is no DOI, derivation notes).
The analysis code uses only `verified` rows; every row shipped in this package is `pilot_unverified`, so no Z effect size is computed until re-extraction (charter SC1).

## grade_draft.csv
Header template: schema/grade_draft.csv (21 columns, in this order); live file reporting/grade_draft.csv, one row per ability × primary outcome, written by the appraisal skill.

| Field | Meaning / allowed values |
|---|---|
| ability_id | A01–A26 |
| outcome | the primary row's `outcome_measure` string, copied exactly, so that 04_sof.R can join on ability_id + outcome |
| n_studies | number of studies contributing to this ability × outcome (k of the pooled unit, or 1) |
| n_participants | sum of analysed participants across those studies |
| design_mix | semicolon-separated design counts (`rct:2;pre_post:3`) |
| starting_level | `High`, `Low`, `Very low` (rule in skills/appraisal/SKILL.md) |
| rob_downgrade, inconsistency_downgrade, indirectness_downgrade, imprecision_downgrade, publication_bias_downgrade | `0`, `-1` or `-2` |
| large_effect_upgrade, dose_response_upgrade, opposing_confounding_upgrade | `0`, `1` or `2`; non-zero only for non-randomised evidence without serious risk of bias |
| draft_certainty | `High`, `Moderate`, `Low`, `Very low`: the arithmetic result of starting level plus downgrades and upgrades |
| reasons | one sentence per non-zero domain naming the studies driving it, separated by `;` |
| plain_language_statement | GRADE informative statement for the Summary of Findings |
| rater_id | `agent-appraisal` (or `-A`/`-B`) |
| date | ISO date |
| skill_version | git short hash of skills/appraisal at run time |
| model | exact model string from the run |

## grade_final.csv
Header template: schema/grade_final.csv = the 21 grade_draft.csv columns in the same order plus five; live file reporting/grade_final.csv, written by the subject-matter co-author from the draft (one row per draft row; the draft columns are copied, not edited, so the pair (draft_certainty, final_certainty) gives the GRADE concordance output, reporting/METHODS_PAPER_OUTCOMES.md #6). 04_sof.R reads ability_id, outcome, n_studies, n_participants, final_certainty, reasons, plain_language_statement and joins on ability_id + outcome.

| Field | Meaning / allowed values |
|---|---|
| final_certainty | `High`, `Moderate`, `Low`, `Very low`: the co-author's rating |
| final_rater_id | `human-<initials>` of the subject-matter co-author |
| final_date | ISO date of the final rating |
| change_reason | why final differs from draft; blank when they agree |
| signed | `yes` once the co-author has signed the table for the Summary of Findings, else `no`; 04_sof.R reports unsigned rows |

## Reconciliation files (tools/reconcile.py; procedure in tools/RECONCILIATION.md)
- discrepancies.csv (`reconcile.py diff`): discrepancy_id (`D-0001`…, deterministic for a given pair of input files) · key (the five key fields joined with `|`) · field (a master column, or `row` when the whole row is in one file only) · value_A · value_B · type (`missing_in_A`, `missing_in_B`, `numeric`, `text`, `provenance`).
- adjudication_log.csv (Sean): discrepancy_id · decision (`A`, `B`, `other`) · chosen_value (required for `other`) · adjudicator · date (ISO) · reason. Every discrepancy needs one row; `build` refuses otherwise.
- master_reconciled.csv (`reconcile.py build`): the master_extraction.csv columns, extractor_id `reconciled`, extraction_date = build date, skill_version and model merged as above, is_primary_outcome set from the primary-outcome file (study_id, ability_id, outcome_measure) or left blank with a warning; analysis/00_load.R refuses blank values, so `--primary` is required before analysis. Read by analysis/00_load.R as extraction/master_reconciled.csv.

## Effect-size conventions (computed in analysis code, never by extractors)
analysis/01_effect_sizes.R reads master_reconciled.csv and writes analysis/outputs/effect_sizes.csv with the columns `es_id, study_id, ability_id, outcome_measure, timepoint, design, lever_type, measure, yi, vi, n_i, n_c, is_primary_outcome, synthetic, derivation`. `measure` is one of:
- `SMD` — independent groups (`rct`, `nonrandomised_comparison`): Hedges' g with small-sample correction from means, SDs and n per condition (metafor `escalc(measure = "SMD")`).
- `SMCR` — within-person designs (`pre_post`, `crossover`): standardised mean change using the raw-score (pre) SD, with the pre/post correlation taken from `pre_post_r`. When `pre_post_r` is blank, the placeholder r = 0.5 is used (analysis/constants.R `R_PREPOST_DEFAULT`, placeholder pending the statistician co-author's decision at Gate 5) with sensitivity runs at r = 0.3 and 0.7.
- `PLO` — prevalence designs: logit-transformed proportion from `n_responders`/`n_tested`; back-transformed to a proportion for reporting.
- `OR` — binary outcomes compared across two rows: log odds ratio from the two `n_responders`/`n_tested` pairs.
- `Z` — Δ/σ_pop with delta-method variance Var(z) ≈ Var(Δ)/σ² + Δ²·Var(σ)/σ⁴, Var(σ) ≈ σ²/(2(n_pop − 1)); computed only where a `verified` population_sd.csv row matches the ability_id and unit, in addition to SMD/SMCR for the same pair.
- Conversions, recorded in `derivation`: SE → SD, sd = se·√n; CI95 → SD, sd = (hi − lo)/(2·1.96)·√n. No other interval is converted.
- `synthetic` is `yes` when study_id starts with `synth_`; synthetic rows never enter a reported table.

Pooling unit: ability_id × measure, using rows with `is_primary_outcome = yes` only; non-primary rows are reported individually (freq_individual.csv) and never pooled. Frequentist pooling at k ≥ 3 (charter D1); below that, individual intervals plus the Bayesian posterior. Dependent effect sizes within a pooling unit (several timepoints or conditions of one study) are a known limitation; the multilevel alternative is a Gate 5 decision. Bayesian pooling runs only on SMD/SMCR/Z measures under the declared SMD-scale priors; PLO/OR rows get a note row ("Beta-binomial / logit model: Gate 5").
