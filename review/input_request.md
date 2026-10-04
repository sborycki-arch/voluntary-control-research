# Input request — pass 5 (2026-10-04)

Struck items were supplied; remaining items are still needed. Grouped by supplier.

## Supplied by Sean
| # | Item | Status (pass 5) | Still needed for |
|---|---|---|---|
| S1–S4 | ~~Plan, research document, evidence map, failure log~~ | Supplied (pass 2) | — |
| S5 | Full texts for the dry-run candidates (Kozhevnikov 2013 open access; Zeidan 2011; Meissner 2024; Code 1995; Eberhardt 2021; Manuck 1976) staged under extraction/fulltext/ with access_route, and the five chosen rows in dry-run/selection.csv | Still missing | R-029; precision-rule confirmation (R-054); dry run |
| S6 | ~~Gate 0 tracker state~~ | Supplied (pass 5): the reviewer read the live plan at rev 13; G0 "Approved" (dropdown index 2). The bundle's stale GATE_LOG.md moved to S10 (R-048 D-i) | — |
| S7 | Primary texts of the cited standards (PRISMA-trAIce; Ding et al. 2026; RAISE v3; ICMJE Jan 2026; Minozzi 2020; BARG; PRISMA 2020/P; Cochrane/Campbell/JBI/CEE 2025; COPE 2023; RoB 2 / ROBINS-I / JBI documents) | Still missing | R-033, R-034, R-035, R-036, R-037; checklist audit |
| S8 | Environment route decision and the machine that will pin it (CRAN reachability; git) | Still missing | R-038, R-015, R-016, R-076 |
| S9 | Co-author status | Still missing | owners of R-012, R-023, R-025, R-040, R-074, R-071 |
| S10 | Repository integration decisions. Reported decided in commit 9c09e2c (Sean, 2026-10-04): the live plan is the only gate tracker; the research repository is sborycki-arch/voluntary-control-research (private), with gates/GATE_LOG.md as a pointer and this package unmerged on branch stage1-package. Still needed: copies of the pointer GATE_LOG.md and of CLAUDE.md as they stand in that repository (the reviewer cannot open it); the CLAUDE.md gate-rule revision; gate-package location and naming; analysis/ and data/ split; repository map | Partly supplied | R-047, R-048, R-049, R-050, R-061 |
| S11 | Methods-paper scope | Still missing | R-058 |
| S12 | Rulings on plan departures and builder actions awaiting confirmation: R-021 (subset coders; skill text already changed), R-068 (validated self-report outcomes; criteria already redrafted), R-044, R-045, R-046, R-027, R-020/R-060 (extraction κ) | Still missing | register closure; skill revisions if returned |
| S13 (new) | Acceptance or rejection of the retroactive build-run record (role field contradicts its stand-in; absolute paths) and transcript policy (platform_export vs final_report_only) | New | R-001, R-007 |
| S14 | Commit-identity convention for agent commits | Partly answered: new commits carry an agent identity (5fd00ef); the six round-2 commits keep Sean's name; the convention for the merged repository is still Sean's | R-079 |
| S15 (new) | Confirmation that Sean saved the G0 dropdown at rev 13 (the read shows no editor) | New | G1 verification note |

## Supplied by the builder
| # | Item | Status | Still needed for |
|---|---|---|---|
| B1 | ~~Trace record of the build run~~ | Retroactive record written (verified); acceptance is Sean's | R-001 |
| B2 | ~~Smoke-test artefacts~~ | Supplied: traces/test_trace_logger.py (45 ok) | — |
| B3 | ~~Git state / skill hashes~~ | Supplied: repository with commits; fixer records carry hashes | — |
| B4 | ~~Staging of the other skills~~ | Answered by the plan (Stages 2–7) and OPEN_DECISIONS; dry-run step 5 no longer depends on a statistician agent | R-032 stays Sean's |
| B5 (new) | Fixes for R-078, R-080, R-081, R-082, R-083 (minor) and the R-037 GRADE-row template reference | New | next fix round |
| B6 (new) | Transcripts attached (platform_export) for every run from the dry run on, with the file location written into TRACE_SPEC | New | R-007 |

## Supplied by the statistician co-author (when recruited)
| T1 | Analysis plan: pre/post correlation rule (placeholder r = 0.5), dependent effect sizes, prevalence/binary Bayesian model, thresholds, sensitivity set, Z rows for n = 1 and dual SMD/Z units | R-011 (confirm), R-012, R-016, R-025, R-069 placeholder, R-070 |

## Supplied by the subject-matter co-author (when recruited)
| M1 | Tool mapping for pre_post/other designs; GRADE starting level for case reports and prevalence surveys; blind-first rating on a subset | R-023, R-074, R-071 |
