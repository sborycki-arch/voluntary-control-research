# Gate log

Sean edits the Status column. Allowed values: `Not submitted`, `Awaiting approval`, `Approved`, `Returned`. Claude never writes `Approved`.

| Gate | Stage it opens | Status | Decided on | Note |
| --- | --- | --- | --- | --- |
| G0 Charter | Stage 1, team and tooling | Awaiting approval | | Plan: docs/research-team-plan.md; decisions in its Section 10 |
| G1 Team and tooling | Stage 2, protocol and registration | Not submitted | | |
| G2 Protocol and pre-registration | Stage 3, search and screening | Not submitted | | |
| G3 Search and screening | Stage 4, extraction and risk of bias | Not submitted | | |
| G4 Extraction and risk of bias | Stage 5, analysis plan | Not submitted | | |
| G5 Analysis plan lock | Stage 6, results | Not submitted | | |
| G6 Results | Stage 7, manuscript | Not submitted | | |
| G7 Manuscript | Submission by Sean | Not submitted | | |
| G8 Primary study go/no-go | Phase 2 (own gate plan) | Not submitted | | |

## Gate 0 decisions
- [ ] Scope of the review: all 26 abilities, or lever-free effectors only with the rest as a secondary table
- [ ] Target journal tier (general medical/physiology vs specialist psychophysiology)
- [ ] Human co-authors: statistician and subject-matter expert named, or recruit before G2
- [ ] Database access: Embase, PsycINFO, Web of Science available, or PubMed/Scopus/Google Scholar only
- [ ] Approve the weekly monitor task after G1, and multi-agent workflows at G3 and G4
- [ ] Bayesian priors: accept defaults (μ ~ N(0,1), τ ~ half-N(0,0.5)) or statistician-set

## Gate packages
Each package has four parts: deliverable, verification note (what was checked and how), adversarial reviewer report, open questions. Store packages under `gates/packages/G<n>-<YYYY-MM-DD>/`.
