# Pre-specified measured outputs for the methods paper

Filed before Gate 3 as a supplement to the registered protocol, so that the methods paper's claims are not chosen after the fact. Each output has its computation and its data source.

| # | Output | Computation | Source |
|---|---|---|---|
| 1 | Citation-verification rate | References confirmed by DOI resolution / all references, by route (Crossref, OpenAlex, publisher page); unresolved list published | citation agent log |
| 2 | Screening agreement, agent–agent | Cohen's κ at title/abstract and at full text; disagreement count and resolution | screening_decisions.csv (A, B) |
| 3 | Screening agreement, agent–human | Cohen's κ on the seeded blind subset of 10–20% of records (charter D4), coded by the co-authors (the statistician co-author and the subject-matter co-author; seed in trace; Sean adjudicates and does not code); agent sensitivity and specificity against the human-adjudicated final include set | subset decisions (`screener_id = human-<initials>`); final include list |
| 4 | Extraction agreement | Agent–agent: field-level exact-agreement rate; numeric discrepancy rate; discrepancies by type (misread, wrong row, unit, omission); error rate found in the statistician's spot-check. Agent–human: field-level exact-agreement rate and numeric discrepancy rate of the reconciled agent file against the co-authors' blind extraction of the 10–20% subset of included studies (charter D4; procedure in skills/extraction/SKILL.md "Blind human subset"; tools/reconcile.py diff), reported alongside the agent–agent figures | master A vs B; human subset file (`extractor_id = human-<initials>`) vs master_reconciled.csv; adjudication log |
| 5 | Risk-of-bias agreement | Agent-draft vs co-author-final agreement per domain and overall (κ). Benchmark: Minozzi et al. 2020 human–human RoB 2 κ 0.16 — **unverified: primary not opened from the build environment** (R-036; cite only after the primary is read at G2). Independence of the human rating from the agent draft is an open design question (R-071); the comparison with Minozzi 2020 is not valid unless the human rating is blind-first | appraisal.csv (agent, human) |
| 6 | GRADE concordance | Agent draft certainty vs signed final certainty per ability × outcome: exact agreement, linearly weighted κ, direction and reason of each disagreement. Independence of the human rating from the agent draft is an open design question (R-071); the comparison with Minozzi 2020 is not valid unless the human rating is blind-first | grade_draft.csv vs grade_final.csv |
| 7 | Reproduction | Share of tables and figures that rebuild identically from the raw file in the reviewer's fresh session | reviewer report, MANIFEST.sha256 |
| 8 | Failure log | Safety-filter stops, access blocks, fabricated or wrong citations caught by the reviewer, numbers that failed reproduction, prompt revisions after use | traces/, reviewer reports |
| 9 | Effort and cost | Agent runs, tokens and cost per stage where exposed; human hours per stage (Sean and co-authors log them) | traces/, time log |
| 10 | Standards compliance | PRISMA 2020, PRISMA-trAIce, RAISE 2026 (version as recorded at G2, reporting/REPORTING_PLAN.md), Ding Table 10, BARG items met / not met | reporting/ checklists (templates in reporting/templates/) |

Not an output: any claim that the agents "match" or "beat" human reviewers in general. The comparison population is one review with two human co-authors.
