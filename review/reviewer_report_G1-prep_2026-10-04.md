# Reviewer report — Gate 1 preparation, pass 1 (2026-10-04)

Reviewer: independent reviewer/PM, fresh session, role `reviewer`, trace `s1-reviewer-single-20261004T042044Z-2d52`.
Package reviewed: the Stage 1 build at PKG (57 files), verified byte-identical to the upload `badc0db9-vcr-stage1-build.zip` (sha256 0c3b2b8a…eded2); the only additions after extraction are traces/stage1.jsonl and the reviewer prompt.
Measured against: gate-packages/G0_2026-10-03_charter-decisions.md (decisions 1–7, three Stage 1 additions, two standing conditions) and README.md "Stage 1 status" (eleven Gate 1 rows). Procedure: skills/reviewer/SKILL.md and references/checklists.md as they apply at Gate 1 (steps 1, 3, 5; steps 2 and 4 are Gate 5+).
Not available in this pass: the Claude Research Team Plan, the research document, the evidence map. Their contents are not inferred anywhere below.
Environment: Python 3.11. R was absent at the start of the review; R 4.3.3 with metafor 4.4.0, dplyr, readr, digest, jsonlite, ggplot2, brms and renv became available from apt during the review. CRAN is denied by the session proxy (cloud.r-project.org CONNECT 403); `meta` and `bayesmeta` are not installable, so 02_bayesian.R, run_all.R and setup.R were reviewed by reading only, and 00_load.R, 01_frequentist.R and 03_sof.R were executed on synthetic data on copies under PM/scratch/rtest. Every scholarly host the package cites is blocked by the egress proxy (list in section 2); no external citation could be opened.
Issue ids (R-nnn) refer to PM/issues_register.csv; claim ids (Cnn) to PM/claims_audit_pass1.csv.

## 1. FAIL list

A FAIL is a finding of severity blocker or major. Location | expected | found.

| Id | Location | Expected | Found |
|---|---|---|---|
| R-009 (blocker) | SCHEMA.md:51-54; analysis/01_frequentist.R:4-6; 00_load.R:14-15; run_all.R:1 | Analysis code computes Hedges' g, the z scale (delta-method variance), log OR and logit prevalence from the master file ("computed in analysis code, never by extractors"); run_all.R rebuilds every table from the raw file | No script derives effect sizes. 01_frequentist.R reads a pre-built analysis/outputs/effect_sizes.csv attributed to a "statistician agent" for which no skill exists; population SDs are loaded and never used. The rebuild chain starts downstream of the raw file. Dry-run pass criterion 5 and METHODS_PAPER_OUTCOMES #7 have no mechanism |
| R-001 | charter "Stage 1 scope additions" bullet 1; TRACE_SPEC.md:28; traces/stage1.jsonl | Trace capture from the first agent call; every agent run has a completed record | stage1.jsonl holds one record: the start record of this review. The build run and the smoke test README claims have no record or transcript |
| R-003 | trace_logger.py:40-49 | end() completes a record safely when A and B agents finish concurrently | end() rewrites the whole file without a lock. Scratch test: 60 concurrent end calls → 2 "trace not found" exits; a failed end leaves the record incomplete, which the spec treats as the run not having happened |
| R-004 | TRACE_SPEC.md:13; SCHEMA.md:38; trace_logger.py:17-21; stage1.jsonl | skill_version = git short hash of the skill folder | Package is not a git repository; the existing record carries `no_git`; every dry-run record will too until the project is under git |
| R-006 | TRACE_SPEC.md:20,22,24; trace_logger.py:31,44-47 | tool_calls count and counts by tool; safety_stop with what was being processed; selection_policy from the spec vocabulary | tool_calls is always `{}` (no argument exists); no field for the safety-stop subject; selection_policy is free text |
| R-007 | TRACE_SPEC.md:3,31; traces/transcripts/ | Raw transcript saved as traces/transcripts/<trace_id>.md for every run | Folder empty (only .gitkeep), including for this run; the logger has no transcript handling; no procedure states how a sub-agent transcript is exported |
| R-010 | charter D1; 01_frequentist.R:10 | Abilities below k = 3 get individual-study intervals | A note row "k<3: not pooled; individual intervals reported" only. Executed: A06 (k = 1) produced the note and no intervals |
| R-012 | 03_sof.R:6-8; SCHEMA.md:5; appraisal SKILL.md:33 | Summary of Findings joins each ability × outcome to its own estimate; a rule exists for multiple outcomes/timepoints per study | Join is by ability_id alone. Executed: two outcomes of A03 received the identical pooled estimate. No aggregation rule for dependent effect sizes anywhere |
| R-013 | SCHEMA.md:3; appraisal SKILL.md:34; 03_sof.R:5-8 | Every CSV the pipeline reads or writes has a schema | grade_draft.csv (skill) and grade_final.csv (03_sof.R, columns final_certainty etc.) are defined nowhere; SCHEMA.md says "all four CSV files" |
| R-019 | 00_load.R:3; extraction SKILL.md:8; METHODS_PAPER_OUTCOMES.md:10; DRY_RUN_PROTOCOL.md:22,30 | A defined path from extractor A and B files to extraction/master_reconciled.csv: diff format, adjudication log, discrepancy list | None specified. The "adjudication log" cited as a methods-paper data source does not exist as a format |
| R-020 | charter D4; extraction SKILL.md; METHODS_PAPER_OUTCOMES.md:10 | Co-authors code a blind 10–20% subset giving screening **and extraction** agent-vs-human κ | Blind subset exists for screening only. Extraction has no human subset; outcome #4 reports agent–agent agreement and a spot-check, not κ against humans |
| R-028 | DRY_RUN_PROTOCOL.md:12-18,25; 01_frequentist.R:10-18 | The dry run exercises the analysis code | Five candidates, five abilities, k = 1 each: pooling, LOO, Egger, forest and funnel never run. The "synthetic effect_sizes.csv" has no owner, rule, label or location |
| R-029 | DRY_RUN_PROTOCOL.md:6-18 | Five candidates confirmed `verified` in the research document's table with full text in hand | Research document not available in this pass; 5 of 7 candidates "confirm access"; targets quoted from the pilot, not the papers. Selection cannot be made |
| R-033 | reviewer SKILL.md:18; checklists.md:11; REPORTING_PLAN.md:9 | Published PRISMA-trAIce items available to the reviewer ("do not work from memory") | Neither the item list nor the named checklist template is in the package; primary source unreachable (ai.jmir.org, doi.org blocked). Audit below uses the package's seven-heading paraphrase |
| R-034 | checklists.md:13-19 | Ding et al. Table 10 items quoted from the PDF | Text says "three proposed items", lists five bullets; paper unreachable (arxiv.org blocked). Wording unverified |
| R-038 | README.md:29; ENVIRONMENT.md; setup.R | Pinned R environment (renv.lock, session_info.txt) | Not delivered (README agrees). In this container setup.R cannot run (CRAN 403; bayesmeta/meta not installable). 02_bayesian.R and run_all.R did not execute (verified: both halt on `library(bayesmeta)`) |

Discrepancies of minor severity (not gate-blocking; full text in the register): R-002, R-005, R-008, R-011, R-014, R-015, R-016, R-017, R-018, R-021, R-022, R-023, R-024, R-025, R-026, R-027, R-030, R-031, R-032, R-035, R-036, R-037, R-039, R-040, R-041, R-042.

## 2. Unverified list (not opened, and where I tried)

Each host below was tried once; the egress proxy returned EGRESS_BLOCKED or 403 on CONNECT. Policy denials are not retried.

| Claim(s) | Source | Where tried |
|---|---|---|
| C40 Minozzi 2020, κ 0.16 (95% CI 0.08–0.24), four raters, 70 RCTs | doi:10.1016/j.jclinepi.2020.06.015 | doi.org (blocked); api.crossref.org (CONNECT 403); www.ebi.ac.uk Europe PMC REST (blocked); eutils.ncbi.nlm.nih.gov (blocked) |
| C48, C49 PRISMA 2020 and PRISMA-P item lists | BMJ 372:n71; BMJ 349:g7647 | doi.org; api.crossref.org |
| C50 PRISMA-trAIce item list | JMIR AI 2025, e80247 | ai.jmir.org (blocked); doi.org |
| C51, C58 RAISE 2026 v3 / v3.1 | doi:10.17605/OSF.IO/FWAUD | osf.io (blocked); doi.org |
| C52, C53 Ding et al. 2026 Table 10 | arXiv 2608.05179 | arxiv.org (blocked) |
| C54 BARG | Kruschke 2021, Nat Hum Behav 5:1282–1291 | doi.org; api.crossref.org |
| C55 ICMJE January 2026, II.A.4 and V | icmje.org | www.icmje.org (blocked) |
| C56 COPE 2023 statement | publicationethics.org | blocked |
| C57 Cochrane/Campbell/JBI/CEE 2025 statement | Environ Evid 14:20, doi:10.1186/s13750-025-00374-5 | environmentalevidencejournal.biomedcentral.com (blocked); doi.org |
| C44, C45 RoB 2 domains; ROBINS-I domains and judgments | riskofbias.info | www.riskofbias.info (blocked) |
| C46 JBI checklist names | jbi.global | blocked |
| C47, C74 GRADE handbook; ROBINS-I starting-level convention | gdt.gradepro.org | blocked |
| C59–C65 population_sd.csv sources (Quer 2020; Wright 2011; Geneva 2019; Uematsu 1988; "Sci Rep 2019"; Schroeder 2018; Shahnaz & Ciocca 2026) | DOIs where given | doi.org; journals.plos.org (blocked); four rows have no DOI; one citation is incomplete in the package itself |
| C66–C72 Dry-run candidate values (Kozhevnikov 2013; Zeidan 2011; Meissner 2024; Code 1995; Eberhardt 2021; Manuck 1976; Paravlic 2018) | papers and the research document | journals.plos.org (blocked); other hosts blocked; research document not supplied in pass 1 |
| C06, C41, C42 README and protocol statements attributed to the plan | Claude Research Team Plan | not supplied in pass 1 |
| C09, C10 Known tool limits attributed to the evidence review | evidence review | not supplied in pass 1 |

## 3. Checklist table (Gate 1: PRISMA-trAIce and Ding et al. Table 10; trace completeness)

The PRISMA-trAIce rows use the seven headings in checklists.md:11, which are the package's paraphrase, not the published items (R-033). The Ding rows use the five bullets in checklists.md:14-18 (R-034). Status vocabulary: met (in specification) / not met / not applicable at G1 / cannot be checked before the dry run.

| Checklist | Item (as paraphrased in the package) | Status | Evidence location |
|---|---|---|---|
| PRISMA-trAIce | Tool identity and version | met in specification; content checkable only per run | TRACE_SPEC.md:15 (model string); stage1.jsonl model = claude-fable-5-1 (verified against the platform); REPORTING_PLAN.md:20 |
| PRISMA-trAIce | Stage of use | met in specification | REPORTING_PLAN.md:20 lists every stage and the human role at each |
| PRISMA-trAIce | Prompts and configuration | partly met; cannot be checked before the dry run | TRACE_SPEC.md:14,16 (prompt_ref, prompt_sha256, model_settings); one prompt stored verbatim and hash-verified (C30); no skill prompt has yet been run |
| PRISMA-trAIce | Validation performed | cannot be checked before the dry run | DRY_RUN_PROTOCOL.md pass criteria; METHODS_PAPER_OUTCOMES #2–#7 define the statistics; none computed |
| PRISMA-trAIce | Human oversight | met in specification; no consolidated list (see Ding row 1) | screening SKILL.md:8,20; extraction SKILL.md:8,22,27; appraisal SKILL.md:8,38; charter D4; gates |
| PRISMA-trAIce | Error handling | met in specification | screening E8/unsure (SKILL.md:23); extraction provisional rows (SKILL.md:22; 00_load.R:12-13 executed); safety_stop field (TRACE_SPEC.md:24); MONITOR_SPEC.md:13 |
| PRISMA-trAIce | Limitations | partly met | README.md:43-47 known tool limits (attributed to the evidence review, unverified); ENVIRONMENT.md:3 |
| Ding Table 10 | Human-in-the-loop entry points stated (list) | not met as a list | Entry points are scattered across the four skills and the charter; no single list exists |
| Ding Table 10 | Code released (runnable repository) | not met at G1; cannot be fully checked before the dry run | analysis/ scaffold present; not pinned; raw-to-effect-size step absent (R-009); 02 and run_all do not execute here (R-038) |
| Ding Table 10 | Seeds or execution traces released | partly met in specification | TRACE_SPEC.md; logger functional on a copy (section 9); one record; no transcripts (R-007); screening seed to be recorded in trace (screening SKILL.md:47) |
| Ding Table 10 | Novelty-verification method stated (gap-statement searches) | not applicable at G1 | Stage 2 item (searches/ empty) |
| Ding Table 10 | Number of attempts and selection policy stated | met in specification; cannot be checked before the dry run | TRACE_SPEC.md:22 (run_number, selection_policy, discarded_reason); logger writes them (tested) |
| Reviewer step 5 | Every agent run named in the package has a trace with model, skill version, inputs, outputs, selection policy | not met | Build run untraced (R-001); skill_version = no_git (R-004); transcripts absent (R-007) |

## 4. Counts

Claims audited: 86. Verified: 33 (28 by direct check, 5 by reading R code that could not be executed at the time). Mismatched: 19. Not opened: 34.
Register: 42 findings — 1 blocker, 15 major, 26 minor.

## 5. Judgment

`open failures: 16` (1 blocker, 15 major). The package is not ready to enter a Gate 1 package. Nothing in it violates the standing conditions.

## 6. Charter coverage

| Charter item | Status | Evidence |
|---|---|---|
| D1 Scope: all 26 abilities; pooling at k ≥ 3; k < 3 → individual intervals, Bayesian posterior, GRADE narrative | Partly met | 26 abilities listed (C12; names unverified vs research document). k ≥ 3 rule in code (C13, executed). Individual intervals absent (R-010). Bayesian posterior runs for every ability by reading (02_bayesian.R:10, no k filter; not executed). GRADE drafting per ability × outcome specified (appraisal SKILL.md:33-38). Lever recorded as pre-specified subgroup (extraction SKILL.md:25), consistent with the lever-free question being deferred |
| D2 Registration after Gate 2 | Met (nothing to register yet) | REPORTING_PLAN.md:8 (PRISMA-P at G2); protocol/ empty; no registration artefact |
| D3 Target journals; AI policy read at G2 and G7 | Met in plan | REPORTING_PLAN.md:17 |
| D4 Two human co-authors; blind 10–20% subset for screening and extraction κ; SME adjudicates RoB 2 and signs GRADE | Partly met | Screening subset specified (screening SKILL.md:46-47; outcome #3). Extraction subset absent (R-020). "Sean or a co-author" wording (R-021). SME adjudication and signing specified (appraisal SKILL.md:8,38; 03_sof.R:5) |
| D5 Databases | Consistent so far | Searches are Stage 2 (searches/ empty). Monitor covers the free APIs only and omits two registered sources without saying so (R-026) |
| D6 Priors Normal(0,1), half-Normal(0,0.5); locked at G5 | Met by reading | 02_bayesian.R:5-6 (C15); not executable here |
| D7 Monitor and multi-agent workflows not approved at G0 | Met for the monitor; question for the dry run | MONITOR_SPEC.md:1,14 defers creation; no task exists (C16). Dry run runs dual screeners/extractors (R-027, Sean's ruling) |
| SC1 Pilot table is rationale only | Met | population_sd.csv all pilot_unverified; loader keeps `verified` only (executed: 0 rows loaded). Dry-run targets are a reproduction test, but should be re-anchored to the papers (R-029, R-031) |
| SC2 Nothing submitted, registered, contacted, spent, published or scheduled | Met | No artefact of any such action in the package (C17). This review performed none |
| Addition 1 Trace capture from the first agent call | Not met | R-001, R-003, R-004, R-006, R-007 |
| Addition 2 Reporting plan to PRISMA 2020, PRISMA-trAIce, Ding Table 10, RAISE 2026 v3, BARG | Met as a plan; items unverified | REPORTING_PLAN.md covers all five plus six further standards; no primary could be opened (R-033–R-036) |
| Addition 3 Methods-paper outputs incl. agent-vs-SME GRADE concordance | Met as a plan | METHODS_PAPER_OUTCOMES.md #6; gap in extraction κ (R-020) |

## 7. Consistency: four skills ↔ SCHEMA.md ↔ analysis code

Verified consistent: screening output fields (10 = 10 = 10, C21); master header 37 fields in SCHEMA order (C20); extraction vocabularies (C23); appraisal tool vocabulary (C24); provenance field list between SCHEMA.md and 00_load.R (C19); ENVIRONMENT.md and setup.R package lists (C82); TRACE_SPEC logger usage and argparse options (C75).
Inconsistent: appraisal Output field list omits `notes` (R-014); grade_draft/grade_final undefined and `final_certainty` appears only in 03_sof.R (R-013); `harvest` coding (R-022); appraisal tool mapping lacks `pre_post`/`other` and tool-sources.md names a tool outside the vocabulary (R-023); 0.2/0.5 SD thresholds cited to an analysis plan that does not exist (R-025); abilities.md header names an absent column (R-024); TRACE_SPEC roles without skills (R-032); RAISE version labels (R-035).

## 8. Can the analysis code do what the charter and SCHEMA.md say?

Executed on synthetic data (PM/scratch/rtest; three master rows with full provenance; effect sizes A03 k = 4, A06 k = 1, A10 k = 12):
- 00_load.R: loads complete rows ("Loaded 3 rows, 2 abilities, 0 population-SD rows"); refuses a blank `location` and a row with neither DOI nor URL, writing REFUSED_missing_provenance.csv; stops on an `abstract_only` row. The provenance gate works as SCHEMA.md:3 and README.md:28 state. In a checkout without analysis/outputs/ the refusal path fails on file write before the message (R-017; agrees with the head agent's smoke note, which I treat as the builder's evidence and here confirm).
- 01_frequentist.R: runs on metafor 4.4.0. k = 4: REML + Knapp-Hartung CI, prediction interval, LOO, forest PNG. k = 12: Egger regtest (model rma, predictor sei) and funnel PNG written. k = 1: note row only (R-010). Sensitivity analyses are a comment (R-011).
- 03_sof.R: runs; join by ability_id repeats the pooled estimate across outcomes (R-012).
- 02_bayesian.R and run_all.R: halt at `library(bayesmeta)`; not executable here. By reading, 02 matches charter D6 priors and reports P(μ > 0.2), P(μ > 0.5), a BF and two alternative priors; API usage unverified (R-016).
- setup.R: not executable (CRAN blocked); by reading, renv.lock may omit packages no script loads, and session_info.txt will not carry package versions (R-015).
Conclusion: the scaffold does what its own comments say for the pooling step, but it does not do what SCHEMA.md and run_all.R claim — there is no computation from the raw master to effect sizes (R-009), and the k < 3 and SoF behaviours depart from the charter (R-010, R-012).

## 9. Does trace_logger.py meet TRACE_SPEC.md?

Executed on a copy under PM/scratch (never against PKG): start writes a record with all 26 spec field names; input, prompt and output hashes equal `sha256sum`; end completes ended_at, output_refs, selection_policy, human_intervention, safety_stop, tokens ("not_exposed" default), discarded_reason, notes; unknown trace id exits 1 with a message; `--parent`, `--run`, `--safety-stop`, `--discarded`, token and cost options work; in a git repository skill_version is the short hash of the last commit touching the skill folder, `untracked` for an uncommitted folder, `no_git` outside a repository.
Gaps against the spec: tool_calls never populated and no safety-stop subject field (R-006); no transcript handling (R-007); trace_id `s<stage>` prefix and `stage<N>.jsonl` file name differ from the spec text (R-005); concurrent end() race (R-003); uncaught exceptions on missing paths (R-008); skill_version requires git (R-004).
The record for this run: prompt hash, three input hashes and model string verified (C30–C33, C36); skill_version `no_git` (C37).

## 10. Feasibility of DRY_RUN_PROTOCOL.md as written

Not feasible today. (i) Study selection cannot be made without the research document and confirmed full texts (R-029). (ii) Pass criterion 5 (rebuild from the raw file) cannot be met because no code goes from the master to effect sizes (R-009) and the environment is not pinned (R-038). (iii) Five single-study abilities never exercise the pooling code; the synthetic file that would is undefined (R-028). (iv) Step 5 depends on a statistician agent with no skill (R-032). (v) Trace completeness per pass criterion 3 is impossible until the project is under git and transcripts have a route (R-004, R-007), and the concurrent A/B runs expose R-003. (vi) Reconciliation and the discrepancy list have no format (R-019). (vii) Decoys, κ threshold and selection.csv are unspecified (R-030); derived targets conflict with extraction rule 1 (R-031). (viii) Whether running dual agents in the dry run is within charter D7 is Sean's ruling (R-027). Items (i), (ii), (v) are preconditions; the rest are protocol edits.

## 11. Open questions for Sean

1. Gate 0 authority: the charter record says approved 2026-10-03 "in the project conversation" and that the tracker dropdown is set by you. The tracker was not available to this pass. Does it show Approved? (Pass 2 will record what the uploaded tracker shows.)
2. The build run has no trace record (R-001). Is a retroactive record acceptable, or is the build treated as untraced in the Gate 1 package?
3. Charter D7 versus the dry run's dual screener and extractor agents (R-027): skill test or workflow?
4. Who codes the blind screening subset — the co-authors only (charter) or "Sean or a co-author" (skill)? Your adjudication role conflicts with blinding (R-021).
5. Is extraction agent-vs-human κ (charter D4) still required? If so it needs a procedure (R-020).
6. Environment route (R-038): CRAN-reachable machine with renv; apt-pinned R 4.3.3 without bayesmeta (Bayesian method via brms/Stan); or another environment. Also: is the project under git before the first dry-run call (R-004)?
7. Which five candidates, and can the full texts be staged (R-029)?
8. Can the primary texts of the cited standards be uploaded (R-033, R-034), since this environment cannot reach them?
9. Where are the statistician, search, citation, writer and head skills staged (R-032)?

## 12. Not audited / limits of this pass

- The 26 ability names, synonyms and the dry-run target values were not compared with the research document or evidence map (not supplied).
- No external source was opened; every cited standard and paper is listed in section 2 as not opened.
- 02_bayesian.R, run_all.R and setup.R were read, not run.
- The builder's own review was not seen (withheld by design).
- Checklist audit used the package's paraphrase of PRISMA-trAIce and Ding Table 10, not the published items.
