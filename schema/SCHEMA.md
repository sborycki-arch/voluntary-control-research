# Schema dictionary

All four CSV files are UTF-8, comma-separated, header row as given. The analysis code (analysis/00_load.R) refuses any master row whose provenance fields (source_doi or source_url, location, verbatim_anchor, extractor_id, extraction_date, verification_route) are empty.

## master_extraction.csv — one row per outcome × condition × timepoint
| Field | Meaning / allowed values |
|---|---|
| study_id | `firstauthor_year` plus a letter if needed (`benson_1982a`) |
| record_id | id from the records file |
| ability_id | A01–A26 (skills/screening/references/abilities.md); semicolon-separated if a row informs more than one |
| design | `rct`, `crossover`, `nonrandomised_comparison`, `pre_post`, `case_report`, `case_series`, `prevalence_survey`, `other` (state in notes) |
| population | free text as printed (age, health status, expertise) |
| n_total | total analysed in the study |
| condition_label | `intervention`, `control`, `baseline`, `sham`, or the printed label |
| n_condition | n analysed in this condition |
| comparator_label | label of the row this one is compared with, blank if none |
| lever_type | `feedback`, `breathing`, `muscle`, `imagery`, `suggestion`, `none`, `mixed`, `unclear` |
| outcome_measure | what was measured, as printed (`hearing threshold at 250 Hz`) |
| instrument | device or method (`tympanometry`, `infrared thermistor`) |
| unit | as printed |
| timepoint | as printed (`end of 12 weeks`, `during contraction`) |
| stat_type | `mean`, `median`, `mean_change`, `percent`, `count`, `max_individual`, `other` |
| value | the number as printed |
| dispersion_type | `SD`, `SE`, `CI95`, `IQR`, `range`, `none` |
| dispersion_value | SD/SE/IQR width as printed; for CI use ci_low and ci_high |
| ci_low, ci_high | as printed |
| p_value | as printed (`<0.001`, `0.03`) |
| baseline_value, baseline_dispersion | pre-intervention values on the same row when the paper reports change from baseline |
| n_responders, n_tested | prevalence designs: numerator and denominator |
| value_source | `text`, `table`, `figure`, `supplement`, `derived` |
| derivation | formula and inputs if `derived` |
| source_doi, source_url | at least one required |
| location | page, table, figure or section (`p. 1236, Table 2, row 3`) |
| verbatim_anchor | ≤ 20 words copied exactly from the location |
| extractor_id | `agent-extraction-A`, `agent-extraction-B`, `human-<initials>` |
| extraction_date | ISO date |
| verification_route | `pdf_full_text`, `html_full_text`, `supplement`, `abstract_only`, `not_opened` |
| skill_version | git short hash of skills/extraction at run time |
| model | exact model string from the run |
| notes | free text; reasons for blanks |

## screening_decisions.csv
record_id · stage (`ta`, `ft`) · decision (`include`, `exclude`, `unsure`) · exclusion_code (E1–E8, `harvest`, blank) · rationale (≤ 40 words with a quoted phrase) · confidence (`high`, `medium`, `low`) · screener_id (`agent-screening-A`, `agent-screening-B`, `human-<initials>`) · skill_version · model · timestamp (ISO 8601).

## appraisal.csv
study_id · tool (`rob2`, `rob2_crossover`, `robins_i`, `jbi_case_report`, `jbi_case_series`, `jbi_prevalence`) · tool_version (date or version string) · domain (tool's domain or item name, or `overall`) · judgment (tool vocabulary; see skills/appraisal/SKILL.md) · rationale · source_location · rater_id · date · skill_version · model · notes.

## population_sd.csv
Resting-value sources for the z scale. `status` is `pilot_unverified` until a dual-extracted row with provenance replaces it; the analysis code uses only `verified` rows.

## Effect-size conventions (computed in analysis code, never by extractors)
- Continuous outcomes: Hedges' g with small-sample correction from means, SDs and n per condition.
- z scale: z = Δ / σ_pop with delta-method variance Var(z) ≈ Var(Δ)/σ² + Δ²·Var(σ)/σ⁴, Var(σ) ≈ σ²/(2(n_pop − 1)).
- Binary outcomes: log odds ratio. Prevalence: logit-transformed proportion in a binomial-normal mixed model.
