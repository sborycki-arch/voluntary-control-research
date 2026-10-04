---
name: vcr-appraisal
description: Risk-of-bias appraisal (RoB 2, ROBINS-I, JBI) and GRADE domain drafting for the voluntary-control systematic review. Use this skill whenever you are asked to assess risk of bias, apply RoB 2 or ROBINS-I or a JBI checklist, rate study quality, or draft GRADE certainty for an ability or outcome, even if the request just says "how good is this study".
---

# Appraisal skill

You draft; a human co-author decides. Every judgment you produce is marked `rater_id = agent-appraisal` and is adjudicated by the subject-matter co-author before it enters a Summary of Findings table.

## Tool selection (record the rule used in `notes`)
- Randomised trials, including crossover trials: RoB 2 (crossover variant for crossover designs).
- Non-randomised comparisons of an intervention or exposure with a comparator: ROBINS-I.
- Case reports and case series (including single-person physiological demonstrations): JBI case report / case series checklists.
- Prevalence surveys: JBI prevalence checklist.
- Reviews and meta-analyses: not appraised (screened as `exclude`/E7; their reference lists are mined at Stage 3).

Use the current official tool documents, which are not reproduced in this skill: RoB 2 and ROBINS-I at riskofbias.info; JBI critical appraisal tools at jbi.global/critical-appraisal-tools; GRADE at gdt.gradepro.org (handbook) and the GRADE Book. Record the tool version and access date in `tool_version`.

## Output
Rows in schema/appraisal.csv — one row per study × tool × domain, plus one `overall` row. Fields (identical to the schema/appraisal.csv header, 12 fields): study_id, tool, tool_version, domain, judgment, rationale, source_location, rater_id, date, skill_version, model, notes. Judgment vocabularies:
- RoB 2: `low`, `some concerns`, `high` (domains D1 randomisation, D2 deviations from intended interventions, D3 missing outcome data, D4 outcome measurement, D5 selection of the reported result, overall).
- ROBINS-I: `low`, `moderate`, `serious`, `critical`, `no information` (domains: confounding, selection of participants, classification of interventions, deviations from intended interventions, missing data, outcome measurement, selection of the reported result, overall).
- JBI: per item `yes`, `no`, `unclear`, `not applicable`; overall `include`, `exclude`, `seek further info`.

## Rules
1. Every rationale cites the page, table or figure that supports it (`source_location`). "Not reported" is a finding; write where you looked.
2. Answer the tool's signalling questions in order from the official document; do not skip to the domain judgment.
3. Do not let the size or direction of the effect influence a risk-of-bias judgment.
4. Unregistered or pre-registration-era studies: D5/selection of reported result is at least `some concerns` unless a protocol or pre-specified outcome list is found and cited.
5. Two raters: run as rater A or B when the head agent asks for dual appraisal; otherwise your draft is the single agent draft.
6. Log the run with traces/trace_logger.py (role `appraisal`).

## GRADE domain drafting (per ability × outcome)
Produce a draft row in reporting/grade_draft.csv (header template and field meanings: schema/grade_draft.csv, schema/SCHEMA.md) with: ability_id, outcome, n_studies, n_participants, design_mix, starting_level, rob_downgrade, inconsistency_downgrade, indirectness_downgrade, imprecision_downgrade, publication_bias_downgrade, large_effect_upgrade, dose_response_upgrade, opposing_confounding_upgrade, draft_certainty, reasons, plain_language_statement, rater_id, date, skill_version, model.
- Starting level: `High` for randomised evidence and for ROBINS-I-appraised evidence under that tool's convention; `Low` for other observational evidence; case reports and prevalence surveys start `Very low` to `Low`.
- Each downgrade is `0`, `-1` or `-2` with a one-sentence reason that names the studies driving it. Imprecision is judged against the pooled interval and the 0.2 and 0.5 SD thresholds declared in the analysis plan. Publication bias is `-1` only with a stated basis (funnel asymmetry at k ≥ 10, small-study effects, known unpublished work).
- Upgrades apply only to non-randomised evidence without serious risk of bias.
- The draft certainty is the arithmetic result; the human co-author's final rating may differ and is recorded with a reason. The pair (draft, final) feeds the GRADE concordance analysis in reporting/METHODS_PAPER_OUTCOMES.md.
