# Gate 0 — Charter: decision record

Approved by: Sean Borycki (program lead, sole approver)
Approved: 2026-10-03, in the project conversation. The tracker dropdown in the Claude Research Team Plan (Section "Stage gates") is set by Sean; Claude does not set it.
Scope of this record: the six Gate 0 decisions in the plan's "Decisions needed at Gate 0", plus one added decision (registration) and the Stage 1 scope additions agreed on the same date.

## Decisions as approved

1. Scope of the review: all 26 abilities in the research document. The lever-free restriction is a Gate 8 primary-study decision, not a review decision. Frequentist pooling at k ≥ 3 as planned; abilities below k = 3 get individual-study intervals, the Bayesian posterior and a GRADE-rated narrative synthesis.
2. Registration: PROSPERO (health outcomes present: inflammatory response, blood pressure, pain, seizure frequency). OSF Registries is the fallback if PROSPERO declines the non-clinical abilities. Registration is submitted only after Gate 2 approval.
3. Target journals: the review to a psychophysiology or autonomic journal (Psychophysiology; Autonomic Neuroscience). The methods paper ("Open sourcing health research") to Research Synthesis Methods or Journal of Clinical Epidemiology. Each journal's AI policy is read at Gate 2 and again at Gate 7.
4. Human co-authors: a statistician co-author and a subject-matter co-author (physiology or audiology), both doing real work: they code the blind 10–20% human subset that gives screening and extraction agent-vs-human κ, and the subject-matter co-author adjudicates RoB 2 and signs the GRADE table. Recruitment is Sean's action and starts now; both are needed before Gate 2.
5. Database access: PubMed, Europe PMC, OpenAlex, CENTRAL via the Cochrane Library, ClinicalTrials.gov and preprint servers are registered. Embase, PsycINFO and Scopus are added only if a co-author's institution provides access; otherwise the limitation is stated in the protocol.
6. Bayesian priors: the plan defaults (μ ~ Normal(0, 1) on the SMD scale; τ ~ half-Normal(0, 0.5)) stand until the statistician co-author sets them; locked at Gate 5.
7. Monitor task and multi-agent workflows: not approved at Gate 0. The weekly monitor is a line item at Gate 1; screening and extraction workflows are line items at Gates 3 and 4.

## Stage 1 scope additions (approved with the charter)

- Trace capture from the first agent call: transcripts, pinned model strings, run counts and the selection policy for every agent run (traces/TRACE_SPEC.md).
- Reporting plan built to PRISMA 2020, PRISMA-trAIce, the Ding et al. 2026 Table 10 measured items, RAISE 2026 v3 and BARG (reporting/REPORTING_PLAN.md).
- Pre-specified measured outputs for the methods paper, including an agent-vs-subject-matter-expert GRADE concordance analysis (reporting/METHODS_PAPER_OUTCOMES.md).

## Standing conditions

- The existing scored table (26 abilities; Spearman ρ = −0.60 and −0.81) is a pilot. It enters the protocol as rationale only; no number from it enters results.
- Nothing is submitted, registered, contacted, spent, published or scheduled in Stage 1. Stage 1 ends with the Gate 1 package: skills, schema, environment manifest, dry-run report, monitor specification.
