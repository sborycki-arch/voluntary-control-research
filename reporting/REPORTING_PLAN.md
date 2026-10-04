# Reporting plan

What the review and the methods paper are reported to, with the file that satisfies each item. Items marked "verify" need the primary document checked at Gate 2 (reporting standards change; the landscape review found secondary claims of a "PRISMA 2026" with no primary source).

| Standard | Version to cite | Applies to | Satisfied by |
|---|---|---|---|
| PRISMA 2020 (Page et al. 2021, BMJ 372:n71) | 2020 — verify at G2 whether a 2026 update has a primary DOI | Review manuscript | manuscript/prisma2020_checklist.csv; flow diagram from screening/ counts |
| PRISMA-P (Shamseer et al. 2015, BMJ 349:g7647) | 2015 | Protocol at G2 | protocol/prisma_p_checklist.csv |
| PRISMA-trAIce (JMIR AI 2025, e80247) | 2025 | Both papers | reporting/prisma_traice_checklist.csv (AI tool identity, stages, prompts, validation, oversight, errors, limitations) |
| RAISE 2026 v3 (doi:10.17605/OSF.IO/FWAUD) | v3 / v3.1, 13 March 2026 | Both papers | AI Use Disclosure section (template below) |
| Cochrane/Campbell/JBI/CEE joint position statement (2025; Environ Evid 14:20, doi:10.1186/s13750-025-00374-5) | 2025 | Both papers | AI Use Disclosure section; human oversight statement |
| Ding et al. 2026 Table 10 measured items (arXiv 2608.05179) | v1 | Methods paper | traces/, code release, HITL list, selection policy, novelty (gap) searches |
| BARG (Kruschke 2021, Nat Hum Behav 5:1282–1291) | 2021 | Bayesian results | analysis/02_bayesian.R outputs; prior justification in the analysis plan |
| GRADE handbook / GRADE Book | current at G4 — verify | Summary of Findings | reporting/grade_final.csv (signed) |
| ICMJE Recommendations (January 2026), Section II.A.4 and Section V | Jan 2026 | Submission | AI-use text in cover letter and manuscript; no AI author |
| COPE position statement on authorship and AI (2023) | 2023 | Submission | Author responsibility statement |
| Target journal AI policy | read at G2 and G7 | Submission | manuscript/journal_policy_excerpts.md |

## AI Use Disclosure (template; filled at Gate 7 from the traces)
Tools: Anthropic Claude (model strings as logged in traces/, with dates), used through consumer Claude products (Claude Code with the Agent tool; Claude.ai). Stages: search (agents), title/abstract and full-text screening (two independent agent screeners, human adjudication of disagreements, human-coded blind subset for agreement), data extraction (two independent agent extractors, human adjudication, statistician spot-check), risk-of-bias drafting (agent draft, human co-author final), GRADE drafting (agent draft, human co-author final and signed), statistical code drafting and execution (agent, human statistician review and sign-off), adversarial review (agent in a fresh session), citation verification (agent via Crossref/OpenAlex/publisher pages), manuscript drafting (agent draft, human authors edit and own the text). Validation: dual-agent agreement and agent-vs-human agreement statistics reported in Results and the methods paper; every number carries provenance and was re-derived in a fresh session. Oversight: nine stage gates approved by a named human; gate records released. Inputs and outputs: prompts, traces, transcripts, data and code released at [repository]. The human authors are responsible for all content.

## Methods-section sentence set (PRISMA items 8, 9, 11)
"Two independent AI agents screened all records at title/abstract and full text; disagreements were adjudicated by [SB]. A seeded random x% subset was screened blind by [initials]; agent–human agreement is reported as Cohen's κ. Two independent AI agents extracted data with a mandatory provenance field set; discrepancies (n = …) were adjudicated by [SB] and y% of rows were spot-checked by [statistician]. Risk of bias was drafted by an agent with RoB 2/ROBINS-I/JBI and finalised by [SME]; agent–expert agreement is reported."
