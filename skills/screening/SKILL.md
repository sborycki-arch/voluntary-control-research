---
name: vcr-screening
description: Title/abstract and full-text screening for the voluntary-control systematic review, applied as one of two blinded screeners. Use this skill whenever you are asked to screen records, decide inclusion or exclusion, apply eligibility criteria, or produce rows for screening_decisions.csv for this review, even if the request just says "go through these records" or "which of these are in scope".
---

# Screening skill (one of two blinded screeners)

You are screener A or screener B. You never read, open or ask about the other screener's decisions. The head agent computes agreement afterwards and routes disagreements to Sean.

## Inputs
- A records file (CSV) with at least: record_id, title, abstract, year, authors, source_db, doi (may be blank).
- The stage: `ta` (title and abstract) or `ft` (full text). At `ft` you also receive the full-text path for each record.
- The eligibility criteria. Until Gate 2 registers them, use the DRAFT criteria below. After Gate 2, replace the block with the registered text verbatim and bump `skill_version`.

## Output
One row per record in schema/screening_decisions.csv (see schema/SCHEMA.md). Required fields: record_id, stage, decision, exclusion_code, rationale, confidence, screener_id, skill_version, model, timestamp. Decision values: `include`, `exclude`, `unsure`. Exclusion codes: E1, E2, E3, E4, E5, E7, E8 or blank; there is no other code value (E6 is reserved for the head agent, see below).

## Rules
1. Decide from the record text only. Do not search the web to resolve a record at `ta`; do not open other papers.
2. At `ta`, `unsure` means include for full-text review. At `ft`, `unsure` is allowed only with a rationale stating what is missing; it goes to Sean.
3. Test E7 first: if the record is a review, meta-analysis or overview, write `decision = exclude`, `exclusion_code = E7` and stop; do not go on to the other codes (a review has no primary measurement and no extractable primary result of its own, so E3 and E4 would otherwise fire first and hide the review from reference-list mining). Otherwise apply E1 to E5 in numeric order and record the first that applies; E8 applies only when the full text could not be opened (rule 5).
4. The rationale is at most 40 words and must cite a phrase from the record ("abstract: 'participants were instructed to…'"). Do not paraphrase content that is not in the record.
5. If a full text could not be opened, decision = `unsure`, exclusion_code = `E8`, rationale = where you tried. Never decide from a snippet.
6. Reviews, meta-analyses and narrative overviews are `decision = exclude`, `exclusion_code = E7`. They are not included and are appraised nowhere. The head agent mines the reference lists of all E7 records at Stage 3 (reference-list mining, formerly called "harvest"; `harvest` is not a code value and must not appear in `decision` or `exclusion_code`).
7. One record per row; multi-report studies are linked later by the head agent, not merged by you. You never judge whether a record duplicates another one.
8. Log the run with traces/trace_logger.py before and after (role `screening`, instance A or B).

## DRAFT eligibility criteria (pending Gate 2 registration)
- Population: living humans of any age, healthy or clinical.
- Exposure: a deliberate attempt by the person to change a bodily function in references/abilities.md, with or without a lever (feedback, breathing, muscle tension, imagery, suggestion or hypnosis).
- Comparator: any — within-person baseline or rest, sham, control group, or a population norm — or none for prevalence surveys.
- Outcome: an instrumented physiological measurement, or a validated rating instrument for pain (intensity, unpleasantness) or a seizure diary/count; unvalidated self-report alone is not an outcome. For prevalence designs, the proportion of people who can perform the function counts as the outcome. Aligned to charter D2 (pain and seizure frequency are named health outcomes) and the research document's scope ("measured objectively or by a validated rating"); confirm at G2 (R-068).
- Design: any empirical design including case reports and prevalence surveys. Reviews, meta-analyses and overviews are excluded with E7 (their reference lists are mined by the head agent at Stage 3).
- Language and date: any.

### Exclusion codes, in the order they are tested
- E7 review, meta-analysis or overview → `decision = exclude`, `exclusion_code = E7` (tested first; stop here if it applies)
- E1 non-human or in vitro
- E2 no deliberate attempt by the person (placebo responses, classical conditioning, passive stimulation, drug effects)
- E3 no admissible measurement: neither an instrumented physiological measurement nor a validated rating instrument for pain or a seizure diary/count (unvalidated self-report or observer impression only)
- E4 no extractable quantitative result (no numbers, no figure, no table)
- E5 function not in references/abilities.md and not a reasonable addition (flag additions as `unsure` with the proposed function named)
- E8 full text not obtainable → `decision = unsure`, `exclusion_code = E8`, for Sean

Head-agent code, never applied by a screener: E6 duplicate publication of a record already screened. Deciding E6 needs knowledge of other records, which rules 1 and 7 forbid you. The head agent applies E6 during deduplication of the records file (before `ta` screening and again when linking multi-report studies) and records it under `screener_id = head-agent`.

## Human subset
Before `ta` screening starts, the head agent draws a seeded random 10–20% subset of records (seed recorded in the trace). The two human co-authors (the statistician co-author and the subject-matter co-author; charter D4) screen that subset blind, in the same CSV format with `screener_id = human-<initials>`, so that agent-vs-human κ can be computed at Gate 3 (reporting/METHODS_PAPER_OUTCOMES.md #3). Sean adjudicates agent–agent and agent–human disagreements and therefore does not code the subset. You are not told which records are in the subset.
