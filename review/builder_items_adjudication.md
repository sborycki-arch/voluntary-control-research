# Builder review items — adjudication (pass 3, 2026-10-04)

Reviewer trace: s1-reviewer-single-20261004T112327Z-5788 (run 2; run 1, s1-reviewer-single-20261004T045951Z-5e7b, was terminated by a platform rate limit before output and is logged as discarded). Each builder item was verified against the package independently; nothing was accepted on the builder's or coordinator's word. Executions were on scratch copies under PM/scratch only. Accepted items are register rows with source=builder and the reviewer's severity.

| Builder item | Decision | Register id | Severity | What the reviewer checked | Result |
|---|---|---|---|---|---|
| B-01 Eligibility vs charter (self-report outcomes) | Accepted | R-068 | major | screening SKILL.md:32,39; abilities.md:16,17,19; charter D2; research-project.md:17 (scope admits 'a validated rating'); DRY_RUN_PROTOCOL.md:13 | Confirmed by reading: criteria and E3 exclude pain (A10, A13) and diary-counted seizure frequency (A11); Zeidan 2011 would be E3 at screening. Scope ruling is Sean's; redraft is the builder's |
| B-02 Within-person effect sizes | Accepted | R-069 | major | 01_frequentist.R:5 (escalc SMD); SCHEMA.md:11 (pre_post, crossover), :28 (baseline fields), :52 (g from per-condition means/SDs/n) | Confirmed by reading: no change-SD or pre/post correlation field; no imputation rule. Schema field at G1 (builder); rule at G5 (statistician) |
| B-03 Scale mixing in 02_bayesian.R | Accepted | R-070 | major | 02_bayesian.R:5-17,26; 01_frequentist.R:4-5 | Confirmed by reading: one loop, SMD priors and thresholds for every ability; no measure column to route on; prevalence model deferred by comment only. Not executable here (bayesmeta absent) |
| B-04 Expert-agreement independence | Accepted | R-071 | major | appraisal SKILL.md:8,38; METHODS_PAPER_OUTCOMES.md:11-12 | Confirmed by reading: the co-author adjudicates the draft it is later compared with; benchmark comparison not like for like. Design decision for Sean before the outcomes are filed |
| B-05 Manifest reproducibility | Accepted in part | R-072 | minor | run_all.R:5-6 executed as a listing with a stale MANIFEST present; two runs of 01_frequentist.R on this machine hashed; PNG chunks inspected | Manifest part confirmed: stale MANIFEST.sha256 and the input effect_sizes.csv are hashed. PNG cross-machine instability not verified: byte-identical across two runs here (cairo, no tEXt/tIME chunks); cross-machine untested. Kept as minor with the figure-comparison rule as the actionable point |
| B-06 Exclusion-code ordering; E6 vs rule 7 | Accepted | R-073 | minor | screening SKILL.md:19,21,25,39-43 | Confirmed by reading: E4 (and arguably E3) precede E7 for reviews; E6 needs other-record knowledge against rules 1 and 7. Extends R-022 |
| B-07 GRADE starting-level range | Accepted in part | R-074 | minor | appraisal SKILL.md:35; plan line 60 | Range confirmed and traced to the plan's own wording; discretion effect on concordance follows by reasoning. The GRADE prognosis/prevalence guidance claim is not verified (host blocked). SME decision; extends R-023 |
| B-08 03_sof.R fails at k < 3 everywhere | Accepted | R-075 | major | Executed 01 then 03 on a scratch copy with five abilities at k = 1 | Confirmed: freq_pooled.csv has only ability_id, k, note; 03_sof.R stops with "Column `est` doesn't exist"; run_all.R would fail in the dry-run configuration even with bayesmeta present |
| B-09 renv::restore without load; setup.R stops on brms | Accepted | R-076 | major | Executed renv::restore(project='analysis') from the project root with a stub lockfile: .libPaths() unchanged; renv load() documentation read from the installed package; setup.R:5 read | Confirmed: restored library not used by the session; no fallback in setup.R despite ENVIRONMENT.md:9. Graded major because it defeats the pin that is a Gate 1 deliverable |
| B-10 Logger race, interleaved start/end | Accepted | R-077 | major | 3 trials x 20 concurrent start->end pairs on the scratch copy | Confirmed and extended: trial 2 lost one start record outright; trial 1 produced a torn JSON line (which would crash every later end() at json.loads) plus 8 failed ends; trial 3, 4 failed ends. Extends R-003 |
| R-058 wording note | Agreed | R-058 | minor (was major) | charter D3 and addition 3; plan lines 83, 110; research-project.md:287 | Re-worded as 'plan and research document not amended to carry a charter addition' (class of R-061); severity lowered to minor, gate G2, with the scope-and-workload consequence kept in the row |

Rejected: none. Every item was verified or verified in part; the two partial acceptances (B-05, B-07) record which sub-claims could not be checked from this environment rather than rejecting them.

## Register totals after pass 3
77 findings: 1 blocker, 28 major, 48 minor. By source: reviewer 42, reviewer-pass2 25, builder 10. Open 75, closed 2. Open FAILs (blocker or major): 29 (1 blocker, 28 major).
Judgment line after pass 3: `open failures: 29`.

(Correction note: a first write of this section quoted totals read from an unflushed file; the figures above are from the file as saved.)

## Effect on Gate 1 readiness
- Item 1 (screening skill): R-068 adds a scope defect that excludes three abilities and a dry-run candidate; Sean's ruling needed before the dry run.
- Item 5 (schema): R-069 adds a missing field for within-person designs.
- Item 6 (environment): R-076 means the current run_all.R would not use the pinned library even after pinning.
- Item 9 (dry run): R-075 means run_all.R fails at step 03 in the dry-run configuration; together with R-028 and R-009 the rebuild criterion cannot pass as written.
- Item 10 (traces): R-077 raises the parallel-run risk already in R-003; the dry run's A/B runs must not call the logger concurrently until fixed.

## Questions for Sean arising from this pass
1. R-068: are validated self-report ratings (pain VAS, seizure diaries) admissible outcomes for A10, A11, A13, as the research document's scope says, or are those abilities out of the review?
2. R-071: should the SME co-author produce a blind-first RoB/GRADE rating on a subset before seeing the agent draft, so the methods-paper agreement is independent?
3. R-058 (re-worded): confirm the methods paper stays in scope so the plan can be amended.
