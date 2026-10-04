# Dry run — Gate 1 acceptance test

Plan requirement: "Dry run on five known studies reproduces the numbers already in the research document; every skill tested on one real paper."

## Study selection
Choose five studies that (a) carry `verified` status in the research document's verification table, (b) have full text in hand (open access, or staged by Sean), (c) together cover the design types the appraisal skill must handle, and (d) are not immune-challenge studies (A09 is main-session only). Record the five chosen, with DOI and verification route, in dry-run/selection.csv before any agent runs.

Candidates from the evidence map (pilot values shown are the targets to reproduce; confirm each against the research document first):

| Candidate | Design type exercised | Pilot value to reproduce | Access |
|---|---|---|---|
| Kozhevnikov et al. 2013, PLoS ONE (A03) | non-randomised experiment, ROBINS-I | largest individual axillary rise +2.2 °C; peak 38.3 °C | open access |
| Zeidan et al. 2011, J Neurosci (A10) | within-person pre/post, ROBINS-I | pain intensity −40%, unpleasantness −57% after 4 × 20 min | PMC |
| Meissner et al. 2024, Nat Hum Behav (A08) | randomised, RoB 2 | volitional pupil control after 3 days; randomised 56 + 25 | confirm access |
| Code 1995 (A21) | prevalence survey, JBI prevalence | one ear 22%, both 18%, n = 442 | confirm access |
| Eberhardt et al. 2021, Int J Psychophysiol (A06) | case report, JBI case report | −2.4 mm constriction, +0.8 mm dilation, n = 1 | confirm access |
| Manuck 1976 (A14) | randomised/controlled, RoB 2 | +3.4 bpm raising; lowering not achieved; n = 60 | confirm access |
| Paravlic et al. 2018 meta-analysis (A12) | harvest only; extraction of a pooled estimate for the comparison table | ES 0.72 | confirm access |

## Procedure
1. Screening: both screener agents (A, B) screen the five records plus ten decoy records at `ta`, then the five at `ft`. Head agent computes κ.
2. Extraction: both extractor agents extract the five studies into separate copies of master_extraction.csv. Head agent diffs; discrepancies listed.
3. Appraisal: appraisal agent applies the selected tool to each study and drafts the GRADE row for each ability.
4. Reviewer: reviewer agent, fresh session, audits the five extractions against the full texts and the pilot values.
5. Environment: `Rscript analysis/setup.R`; `Rscript analysis/run_all.R` on a synthetic effect_sizes.csv built from the five studies (statistician agent). Confirm the one-command rebuild and the provenance refusal (delete one location field and confirm the load stops).
6. Every run logged with the trace logger; every prompt stored under traces/prompts/.

## Pass criteria
- All five pilot values reproduced to printed precision, each with a complete provenance block.
- Extractor A and B agree on every target value, or every discrepancy is explained by a documented source ambiguity.
- Each of the four skills executed on at least one real paper, with its trace record complete.
- Reviewer report: no open FAIL on the dry-run package.
- run_all.R rebuilds from the raw file; renv.lock and session_info.txt committed.
- No agent run touched A09 material.

## Report
dry-run/DRY_RUN_REPORT_<date>.md: selection table with verification routes; per-study target vs extracted (A, B); κ; discrepancy list; appraisal rows; reviewer report; environment manifest; trace ids; list of what did not work and why. This report is the core of gate-packages/G1_<date>_team-and-tooling.md.
