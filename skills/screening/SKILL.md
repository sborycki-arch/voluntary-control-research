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
One row per record in schema/screening_decisions.csv (see schema/SCHEMA.md). Required fields: record_id, stage, decision, exclusion_code, rationale, confidence, screener_id, skill_version, model, timestamp. Decision values: `include`, `exclude`, `unsure`.

## Rules
1. Decide from the record text only. Do not search the web to resolve a record at `ta`; do not open other papers.
2. At `ta`, `unsure` means include for full-text review. At `ft`, `unsure` is allowed only with a rationale stating what is missing; it goes to Sean.
3. Apply the exclusion codes in numeric order and record the first that applies.
4. The rationale is at most 40 words and must cite a phrase from the record ("abstract: 'participants were instructed to…'"). Do not paraphrase content that is not in the record.
5. If a full text could not be opened, decision = `unsure`, exclusion_code = `E8`, rationale = where you tried. Never decide from a snippet.
6. Reviews, meta-analyses and narrative overviews are coded `harvest`, not included: their reference lists are mined at Stage 3, and they are appraised nowhere.
7. One record per row; multi-report studies are linked later by the head agent, not merged by you.
8. Log the run with traces/trace_logger.py before and after (role `screening`, instance A or B).

## DRAFT eligibility criteria (pending Gate 2 registration)
- Population: living humans of any age, healthy or clinical.
- Exposure: a deliberate attempt by the person to change a bodily function in references/abilities.md, with or without a lever (feedback, breathing, muscle tension, imagery, suggestion or hypnosis).
- Comparator: any — within-person baseline or rest, sham, control group, or a population norm — or none for prevalence surveys.
- Outcome: an instrumented physiological measurement of the function (or, for prevalence designs, the proportion of people who can perform it). Self-report alone is not an outcome.
- Design: any empirical design including case reports and prevalence surveys. Reviews are `harvest`.
- Language and date: any.

### Exclusion codes
- E1 non-human or in vitro
- E2 no deliberate attempt by the person (placebo responses, classical conditioning, passive stimulation, drug effects)
- E3 no instrumented measurement (self-report or observer impression only)
- E4 no extractable quantitative result (no numbers, no figure, no table)
- E5 function not in references/abilities.md and not a reasonable addition (flag additions as `unsure` with the proposed function named)
- E6 duplicate publication of a record already screened
- E7 review, meta-analysis or overview → code `harvest`
- E8 full text not obtainable → `unsure`, for Sean

## Human subset
Before `ta` screening starts, the head agent draws a seeded random 10–20% subset of records (seed recorded in the trace). Sean or a co-author screens that subset blind, in the same CSV format, so that agent-vs-human κ can be computed at Gate 3. You are not told which records are in the subset.
