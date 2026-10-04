# Open decisions — not pre-empted by the round-2 build (2026-10-04)

Register ids refer to scratchpad/pm/issues_register.csv. Each row below is a decision that belongs to Sean, the subject-matter (SME) co-author or the statistician co-author. The build leaves the governed files as they were, except where noted. Rows are grouped by who decides and the gate at which the decision is needed.

## Sean — needed before the Gate 1 package is assembled

| Id | Decision | Package today | If decided |
|---|---|---|---|
| R-043 | Gate 0 shown as Approved in the tracker. The head agent read the live plan's G0 dropdown as "Approved" at rev 13 on 2026-10-04 (cell msymbcetpvs.11784); the reviewer makes its own observation in pass 5 | Tracker shows Approved (head agent's reading) | Reviewer closes the blocker on its own observation |
| R-048, R-049, R-050, R-047 | Decided by Sean 2026-10-04: the live plan is the only gate tracker; the research repository is sborycki-arch/voluntary-control-research (private), where gates/GATE_LOG.md is now a pointer and this package sits on branch `stage1-package`, unmerged. Still open: one gate-package location and naming (repo `gates/packages/G<n>-<date>/` vs package `gate-packages/G<n>_<date>_<title>.md`); split of pilot code/data (`analysis/evidence.py`, `data/`) from review code/data (`analysis/*.R`, `extraction/`, `schema/`) so SC1 holds; repository map and CLAUDE.md revision for traces/, reporting/, monitor/, dry-run/, schema/; whether the G0 record needs the four-part form | Package layout unchanged | Head agent moves files in one commit after the ruling |
| R-038, R-041 | Environment route: (a) renv on a CRAN-reachable machine, (b) system R 4.3.3 from apt as in this container (metafor 4.4.0; bayesmeta and meta unavailable; Bayesian method via brms/Stan, which apt provides), (c) Python (plan G1 row allows "R or Python"). Scripts now run under (a) or (b) and degrade without bayesmeta | setup.R targets renv; ENVIRONMENT.md documents all three | Pin is produced on the chosen route; renv.lock or an apt manifest committed |
| R-044 | Appraisal skill: include the RoB 2 / ROBINS-I / JBI item lists in the skill (plan Stage 1 wording) or keep URL-only references to the official documents | URL-only | If included: licence check on the tool texts, then the lists are added with version dates |
| R-045 | Dual appraisal: two raters on every study with Sean adjudicating (plan Method 1) or optional dual rating with SME adjudication (package, charter D4) | Optional, SME adjudicates | Skill rule 5 and the G4 workload change |
| R-027 | Is the dry run (two screener and two extractor agents in parallel on 15 records / 5 studies) a skill test (permitted at Stage 1) or operation of the workflows deferred to G3/G4 by charter D7 | Protocol runs A and B in parallel | If workflow: run A then B sequentially, or defer the dual part |
| R-009 (Sean part) | Is a working raw-to-effect-size step required at G1, or is that Stage 5 per the plan? The build implements a first version (analysis/01_effect_sizes.R, labelled pre-G5) because SCHEMA.md and run_all.R claimed it | Implemented, pre-G5 | Statistician co-author reviews it at G5 either way |
| R-029 | Full-text access for the dry-run candidates: only Kozhevnikov 2013 is confirmed open access; Zeidan 2011 (PMC), Meissner 2024, Code 1995, Eberhardt 2021, Manuck 1976 need staging under extraction/fulltext/ | Candidates listed | Dry run can start once five are staged |
| R-032 | Where the search, statistician, citation, writer and monitor skills are built: the plan stages them at Stages 2–7; TRACE_SPEC lists the roles | Four skills only | G1 list unchanged if accepted |
| R-001 (acceptance) | Accept a retroactive trace record for the original build run (written 2026-10-04, timestamps from the zip, model string not recorded) | Record written, `retroactive: true` | Reviewer closes R-001 or it stays as a disclosed gap in the methods paper |
| R-033, R-034 | Primary texts of PRISMA-trAIce (JMIR AI 2025 e80247) and Ding et al. 2026 (arXiv 2608.05179) are unreachable from the build environment; the checklist audit used the package's paraphrase | Templates with headers only | Upload the PDFs; the reviewer re-runs the checklist audit |
| R-021 | Who codes the blind screening subset: charter D4 says the co-authors; Sean adjudicates A/B disagreements so cannot also code it blind | Skill now says co-authors (changed in this round to match the charter) | Confirm |

## Sean — plan amendments (G2 unless stated)

| Id | Amendment |
|---|---|
| R-058 | Methods paper ("Open sourcing health research", charter D3, Stage 1 addition 3) is not in the plan: add it (writer, reviewer, G7 workload, registration supplement) or drop it |
| R-059 | One database list for the protocol: plan G0 decision text, research document Phase 1 (Embase, PsycINFO, Web of Science, Google Scholar) and charter D5 (PubMed, Europe PMC, OpenAlex, CENTRAL, ClinicalTrials.gov, preprints; Embase/PsycINFO/Scopus only with institutional access) disagree |
| R-060, R-061 | Carry the charter's blind human subset, registration decision and three Stage 1 additions into the plan's Stage 1 paragraph and GATE_LOG's decision list (six boxes today) |
| R-062 | Plan says "Eight gates" in the Summary and "Nine gates" in the Stage gates section |
| R-063 | Research document H7 compares the review's correlation with the pilot's; charter SC1 forbids pilot numbers in results. Define H7's comparator without the pilot figure, or amend SC1 |
| R-065 | CLAUDE.md rule 5 ("WebSearch of a bare DOI confirms DOI→title") vs reviewer skill ("snippets are never a source"): clarify that search may confirm bibliographic identity, never a number or quotation |
| R-066 | Plan Stage 1 wording "registered criteria" is impossible before G2; say "draft criteria, replaced verbatim after G2" |
| R-046 | Accept the package's separation of extraction (no RoB items) from appraisal, departing from the plan's team table |
| R-056 | Research repo: data/baselines.csv and analysis/evidence.py still cite "Sci Rep 2019 thermography"; docs/research-project.md [90] identifies Gatt et al. 2019 |
| R-068 | The round-2 screening criteria admit validated pain ratings and seizure diaries as outcomes, following charter D2 and the research document's scope. Confirm at G2 |

## SME co-author

| Id | Decision |
|---|---|
| R-071 | Blind-first rating on a subset so agent-vs-expert agreement (methods-paper outcomes #5, #6) is independent; otherwise the Minozzi 2020 comparison is invalid |
| R-074 | GRADE starting level for case reports and prevalence surveys: the plan's "Very low to Low" range vs a fixed rule; GRADE guidance for prevalence questions to be checked against the handbook |
| R-023 | Tool mapping for `pre_post` and `other` designs; ROBINS-I applicability to uncontrolled before–after studies; whether the JBI quasi-experimental checklist enters the vocabulary |

## Statistician co-author (G5 unless stated)

| Id | Decision |
|---|---|
| R-069 (placeholder) | Pre/post correlation for within-person effect sizes: the build uses r = 0.5 with sensitivity at 0.3 and 0.7 when `pre_post_r` is not printed (analysis/constants.R). Set or replace |
| R-012 | Dependent effect sizes: the build pools one primary outcome per study × ability; a multilevel model is the alternative |
| R-070 | Priors and thresholds for prevalence (logit) and binary (log OR) abilities: the build runs only SMD-scale measures through the declared priors and writes note rows for the rest |
| R-011 | Sensitivity analyses as implemented (fixed-effect comparison; exclusion of n ≤ 3; lever-type subgroup) — confirm the set |
| R-016 | Behaviour of the Bayesian model at k = 1; prior predictive check (BARG) |
| R-025 | Imprecision thresholds 0.2 and 0.5 SD are in analysis/constants.R; the analysis plan that declares them is a G5 deliverable |
| R-040 | Population-SD rows stay `pilot_unverified` until dual-extracted with provenance (G4) |

## Questions raised by the round-2 fixers (recorded in build-log/CHANGELOG_A–D.md)

| Raised by | Question | Owner |
|---|---|---|
| A | Transcript policy from the dry run on: require a platform transcript export for every sub-agent run, or accept the agent's hand-back text (`final_report_only`) where the head agent cannot reach the platform file? No run so far has a transcript attached | Sean |
| A | The retroactive build-run record carries `agent_role = head` although its stand-in prompt says a separate builder agent built the package; records are never edited. Accept as is, or write a second retroactive record with role `builder`? | Sean |
| B | Case reports and n = 1 rows receive a Z effect size with Var(Δ) = 2σ²/n (placeholder). Keep a Z row for single-participant observations, or report them narratively only? | Statistician |
| B | Z rows are written beside SMD/SMCR for the same pair whenever a verified population-SD row matches, giving two pooling units per ability; should the Summary of Findings carry both or name a primary scale per ability? | Statistician |
| B | SMCR convention: (post − pre)/SD_pre with r from `pre_post_r` or the 0.5 placeholder; or SMCC where papers print the SD of change? | Statistician |
| B / C | `grade_final.outcome` must equal the primary row's `outcome_measure` string exactly for the SoF join; a normalisation rule or outcome id set at reconciliation would be more robust. Who sets it, and where is the pre-specified primary-outcome hierarchy written (protocol, G2)? | Sean / SME |
| B | Lever-type subgroup threshold (≥ 2 levels each with k ≥ 2) and the small-study cut (n ≤ 3) sit in analysis/constants.R | Statistician |
| C | Adjudication-log reason vocabulary (misread, wrong row, unit, omission, source ambiguity, other) proposed in tools/RECONCILIATION.md; confirm before the dry run | Sean |
| C | reconcile.py does not diff extractor_id, extraction_date, skill_version, model (they always differ) and writes `extractor_id = reconciled` on reconciled rows; confirm | Sean |
| D | Decoys 8–10 (Goebel 2002, Albring 2012, Kirchhof 2018) are immune-conditioning records (not A09 endotoxin studies, screened from record text only); keep them, given the plan's note on safety-filter stops on immune material? | Sean |
| D | Should the dry run also exercise the E8 route (full text unobtainable) by withholding one record's full text at `ft`? | Sean |

## Added after reviewer pass 4 (2026-10-04)

| Id | Decision | Owner |
|---|---|---|
| R-079 | Commit identity: the six round-2 commits were authored under Sean's name because the head agent configured git that way; the working copy now commits as "VCR head agent (Claude) <noreply@anthropic.com>". Rewriting the six commits would change every hash cited in the reviewer's reports and trace notes, so they are left as they are. Convention for the merged repository (author = agent identity, Sean as committer or sign-off?) before any merge or release | Sean |
| R-007 (policy) | Platform transcripts exist for the nine round-2 fixer/verifier runs (JSONL, 6.6 MB in total, under the session's workflow directory) and can be attached with `trace_logger.py end --transcript`; the reviewer's own runs have only their hand-back text. Require platform exports where they exist and `final_report_only` otherwise, from the dry run on? Released at Gate 7 per TRACE_SPEC, so size and content (they contain full tool output) matter | Sean |

## Not decisions — carried as known limits

- R-035, R-036: RAISE version and Minozzi 2020 figures stay marked unverified until the primary documents are opened.
- R-064: the dry-run access plan now lists every host that failed in the evidence review.
