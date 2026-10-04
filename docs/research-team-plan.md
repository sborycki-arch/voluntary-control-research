# Claude Research Team Plan

Oct 3, 2026 · Sean Borycki

Live document (with the gate-approval dropdowns and diagrams): https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2

## Summary

This plan runs the voluntary-control research programme as a stage-gated project in which a team of Claude agents does the searching, extraction, statistics and drafting, and nothing passes a gate without Sean's written approval in the tracker below. Eight gates separate charter, team setup, protocol and pre-registration, search and screening, extraction and risk of bias, the statistical analysis plan, results, and manuscript submission.

The programme replaces the working certainty and strength rubric from the evidence review with three methods that journals already accept: GRADE certainty ratings built on Cochrane RoB 2, ROBINS-I and JBI appraisal; frequentist random-effects meta-analysis with Hartung-Knapp confidence intervals and prediction intervals; and Bayesian hierarchical meta-analysis reporting posterior probabilities of effect. Each method is specified in Section 4 with its software and its reporting standard (PRISMA 2020, PROSPERO registration, GRADE Summary of Findings).

Claude's role is instrument, not author. Journals require human authors who take responsibility for the work and a disclosure of how AI was used; the plan is built so that every number has a human-approved provenance chain from source page to manuscript table. The companion documents are the Voluntary Body Control Research Project (evidence base and protocol) and the Voluntary Control Terrain map.

## Operating principles

Sean is the sole approver; a gate is passed only when he sets its status to Approved in the Section 5 tracker, and work on the next stage starts only after that.

- **Approval authority.** Each gate has a named deliverable and acceptance criteria. Claude presents the deliverable, states what was verified and what was not, and stops. A gate returned with comments is reworked and resubmitted; nothing downstream is started on speculation.
- **What Claude never does on its own.** Submit a manuscript, register a protocol, contact a journal, co-author, institution or participant, spend money, create a public artifact, or start a multi-agent workflow or scheduled task that was not named in an approved stage. Any of these appears as a line item at a gate.
- **Authorship and disclosure.** The ICMJE recommendations and the COPE position statement hold that AI tools cannot be authors, that human authors are responsible for every part of the work, and that AI use must be disclosed in the manuscript ([ICMJE](https://www.icmje.org/recommendations/), [COPE](https://publicationethics.org/cope-position-statements/ai-author)). The plan therefore names a human author for every section and keeps a log of what Claude generated, which the Methods section will describe. Target journals' AI policies are checked at Gate 2 and again at Gate 7.
- **Pre-registration.** The systematic review is registered on PROSPERO before screening; the primary study is registered on OSF before data collection; every deviation is logged with its date and reason and reported.
- **Provenance.** Every number entering an analysis carries its source DOI or URL, the page or table it came from, who extracted it (agent or person), when, and whether a second extractor agreed. A number without that chain does not enter a table.
- **Reproducibility.** Analysis code in R (metafor, meta, brms) or Python with pinned versions, run from the raw extraction file, with a one-command rebuild of every table and figure; code and data are released at publication.
- **Honesty about tool limits.** Where a source could not be opened, the record says so and the number is marked unverified; search snippets are never treated as sources.
- **Scope of this plan.** Decisions about the science (which effectors, which outcomes) stay in the Voluntary Body Control Research Project; this document governs how the team works and when Sean decides.

## Team architecture

One head agent coordinates nine specialist roles; every output passes an adversarial reviewer before it reaches Sean as a gate package, and the Claude Project holds the shared record.

[Diagram in the live document: Sean above the head agent; search, screening ×2, extraction ×2, appraisal and statistician agents beneath it; citation checks and the writer feeding the adversarial reviewer; the reviewer's report into the gate package; the gate package returning to Sean for approval or return; the Claude Project as the shared store under everything.]

| Role | What it does | Claude tool | Human counterpart |
| --- | --- | --- | --- |
| Program lead | Approves gates, owns authorship, decides the science | Tracker in this doc; comments in the Project docs | Sean |
| Head agent | Plans each stage, assigns work, reconciles outputs, assembles the gate package | Main session with the Agent tool; Project docs and memory | Sean reviews the package |
| Search agents (parallel) | Run the registered search strings per database, deduplicate, export records with dates | Agent tool with WebSearch and WebFetch; database exports staged from the connected computer | Librarian check of the strings at Gate 2 |
| Screening agents (two, independent) | Title/abstract then full-text screening against the registered criteria; disagreements listed | Two Agent runs with a screening skill; blinded to each other | Sean adjudicates disagreements |
| Extraction agents (two, independent) | Extract effect, SD, n, design and risk-of-bias items with provenance into the master CSV | Two Agent runs with an extraction skill | Sean adjudicates; statistician co-author spot-checks |
| Risk-of-bias agent | Applies RoB 2, ROBINS-I or JBI per study and drafts the GRADE domains | Agent with the appraisal skill | Human co-author signs the GRADE table |
| Statistician agent | Writes and runs the analysis code, produces forest plots, prediction intervals, posteriors and Summary of Findings tables | Sandbox shell with R (metafor, meta, brms) or Python; outputs to the Project | Statistician co-author reviews code and plan |
| Adversarial reviewer | Rechecks every claim against its source, reruns the numbers, applies the PRISMA checklist, reports what fails | Fresh Agent run with a reviewer skill, no access to the drafting context | Sean reads the report before deciding |
| Citation-verification agent | Confirms DOI, title, journal, volume, pages for every reference; marks what could not be opened | WebFetch to Crossref, OpenAlex and publisher pages, paced for rate limits | None |
| Writer agent | Drafts manuscript sections in Claude Docs to the journal's format | Claude Docs; style and reporting skills | Human authors edit and own the text |
| Monitor | Weekly literature alert on the registered terms and a citation-health check | Scheduled task, created only after Gate 1 approval | Sean reads the digest |

Two human roles are outside Claude's reach and are recommended before Gate 2: a statistician co-author who signs the analysis plan, and a subject-matter co-author (audiology or physiology) for the primary study; journals will expect both.

## The three certainty methods

The working rubric (High, Moderate, Low; strength in SD units) is replaced by three methods that reviewers already know how to judge: GRADE for certainty, frequentist random-effects meta-analysis for pooled effect and heterogeneity, and Bayesian hierarchical meta-analysis for probability statements and for the small-study cases where frequentist pooling is unstable.

| Method | Question it answers | Inputs | Outputs | Software | Reporting standard |
| --- | --- | --- | --- | --- | --- |
| 1. GRADE with RoB 2, ROBINS-I and JBI appraisal | How certain are we that the effect estimate is right? | Study design, risk-of-bias judgments, consistency, directness, precision, publication bias | Certainty level per outcome (High, Moderate, Low, Very low) with the reason for each downgrade; Summary of Findings table | GRADEpro GDT or a structured table; RoB 2 and ROBINS-I templates | GRADE handbook; PRISMA 2020 items 13f and 15 |
| 2. Frequentist random-effects meta-analysis | How big is the effect, how much do studies disagree, and what would the next study show? | Effect size and standard error per study (Hedges' g, log OR, or transformed prevalence) | Pooled estimate with Hartung-Knapp 95% CI, 95% prediction interval, τ², I², funnel and Egger test when k ≥ 10, leave-one-out | R metafor and meta (REML, HKSJ) | PRISMA 2020; forest and funnel plots |
| 3. Bayesian hierarchical meta-analysis | What is the probability the effect exceeds a threshold, given weakly informative priors? | Same per-study data; prior on μ and τ declared in the analysis plan | Posterior mean and 95% credible interval, P(μ > 0.2) and P(μ > 0.5), posterior predictive for a new study, Bayes factor, prior sensitivity | R bayesmeta or brms (Stan) | Bayesian Analysis Reporting Guidelines (Kruschke 2021) |

**Method 1, GRADE.** Each outcome starts at High certainty for randomised evidence and is downgraded one or two levels for risk of bias, inconsistency, indirectness, imprecision or publication bias, and upgraded for a large effect, a dose-response gradient or opposing confounding. Non-randomised studies are appraised with ROBINS-I and start at High under that tool's convention; case reports and prevalence surveys use the JBI checklists and are rated as Very low to Low unless a large, consistent effect justifies more. Two raters assess every study; disagreements go to Sean with both rationales. The Summary of Findings table reports, per ability, the number of studies and participants, the effect with its interval, the certainty level and the plain-language statement.

**Method 2, frequentist pooling.** Continuous outcomes are pooled as Hedges' g with small-sample correction; binary outcomes as log odds ratios; prevalence with a logit transformation in a binomial-normal mixed model. Between-study variance is estimated by REML, confidence intervals use the Hartung-Knapp-Sidik-Jonkman adjustment, and every pooled estimate carries a 95% prediction interval. Pooling needs at least three studies; below that, studies are reported individually with their own intervals. Pre-specified subgroups: lever type (feedback, breathing, muscle, imagery or suggestion, none). Sensitivity analyses: leave-one-out, exclusion of studies with n ≤ 3, and a fixed-effect comparison. The strength score itself gets an interval: the uncertainty in the population SD is propagated to z by the delta method, so a 4.4 SD claim is reported as 4.4 with its interval rather than a bare number.

**Method 3, Bayesian pooling.** The model is y_i ~ Normal(θ_i, s_i²), θ_i ~ Normal(μ, τ²), with μ ~ Normal(0, 1) on the SMD scale and τ ~ half-Normal(0, 0.5), both declared in the analysis plan before any data are entered, and two alternative priors run as sensitivity checks. Outputs are the posterior for μ, the probability that μ exceeds 0.2 and 0.5 SD, the posterior predictive distribution for a new study, and a Bayes factor for the presence of an effect. For prevalence, a Beta-binomial hierarchical model gives the posterior for population prevalence. This is the method that handles the one-, two- and three-study abilities honestly: with k < 5 the frequentist τ² is unstable, while the Bayesian posterior shows exactly how much the prior is doing.

**Mapping from the working rubric.** Working High maps to GRADE High or Moderate; working Moderate to GRADE Low; working Low to Very low; "Not supported" becomes an estimate near zero with its own certainty level rather than a category. The strength band (Small, Moderate, Large, Extreme) is kept as a display label, but the number reported is the pooled g or z with its interval and its posterior probability.

**Why three and not one.** GRADE answers the certainty question in the language reviewers use; frequentist pooling gives the headline estimate and heterogeneity that PRISMA requires; Bayesian pooling gives probability statements and survives small k. Where the three disagree about an ability, the disagreement is itself a finding and is reported.

## Stage gates

Nine gates; Sean sets the Approval column, and the next stage starts only on Approved. Gate 0 is this plan and is awaiting his decision now. (In this file the approval column is plain text and is not updated; the dropdown in the live document is the only gate tracker, and `gates/GATE_LOG.md` points to it.)

| Gate | Weeks | Deliverable | Acceptance criteria | Approval |
| --- | --- | --- | --- | --- |
| G0 Charter | 0 | This plan plus the Voluntary Body Control Research Project document | Scope, the three methods, team design and gate rules agreed; co-author plan agreed; decisions in Section 10 answered | Awaiting approval |
| G1 Team and tooling | 1 to 2 | Screening, extraction, appraisal and reviewer skills written; master CSV schema with provenance fields; pinned R or Python environment; Project folder structure; monitor task specification | Dry run on five known studies reproduces the numbers already in the research document; every skill tested on one real paper | Not submitted |
| G2 Protocol and pre-registration | 3 to 4 | PROSPERO-ready protocol (eligibility, search strings per database, outcomes, risk-of-bias tools, synthesis plan with the three methods and declared priors); OSF registration text for the primary study; journal shortlist with each journal's AI policy | Sean and the statistician co-author sign; registrations are submitted only after approval | Not submitted |
| G3 Search and screening | 5 to 8 | PRISMA flow counts; deduplication log; dual-screening agreement (Cohen's κ); included-study list; full-text exclusions with reasons | κ ≥ 0.6 at title and abstract or every disagreement adjudicated by Sean; full text in hand for every included study | Not submitted |
| G4 Extraction and risk of bias | 8 to 11 | Master CSV with provenance; dual-extraction discrepancy report; RoB 2, ROBINS-I and JBI tables; draft GRADE domain judgments | 100% of numbers carry source, location, extractor and date; all conflicts adjudicated; discrepancy rate reported | Not submitted |
| G5 Analysis plan lock | 11 to 12 | Statistical analysis plan; code run end-to-end on synthetic data; priors, subgroups, sensitivity analyses and figure templates fixed | Statistician co-author approves; plan time-stamped before any real data are analysed | Not submitted |
| G6 Results | 13 to 15 | All three methods run; Summary of Findings tables; forest, funnel and posterior plots; deviations log; adversarial reviewer report | Reviewer report has no open failure; every table and figure rebuilds from the raw file with one command | Not submitted |
| G7 Manuscript | 16 to 18 | Manuscript to the PRISMA 2020 checklist; AI-use statement; author contributions; data and code release package; cover letter | Human authors approve every section; Sean submits | Not submitted |
| G8 Primary study go/no-go | after G7 | Phase 2 protocol, IRB package, budget and its own gate plan | Decision to proceed, defer or stop, taken on the review's results | Not submitted |

A gate package always has the same four parts: the deliverable, a verification note stating what was checked and how, the adversarial reviewer's report, and a list of open questions. Claude does not mark a gate Approved; only Sean does.

## Stage-gate roadmap

[Roadmap in the live document: seven stage bands on a week axis 0 to 18 with gate diamonds at weeks 0, 2, 4, 8, 11, 12, 15 and 18; G8 follows G7 once the review has reported.]

Stages 3 and 4 overlap by one week because extraction of the first included studies can start while the last full texts are screened; stages 4 and 5 overlap by one week for the same reason. Each diamond is an approval, and the one-week overlaps are the only slack in the 18 weeks.

## Work plan by stage

Each stage ends with a gate package; the tools named here are the ones already used in this session, so nothing depends on capability that has not been demonstrated.

**Stage 1, team and tooling (weeks 1 to 2).** The head agent writes four skills as SKILL.md files: screening (the registered criteria as a decision list), extraction (field by field, with the provenance block mandatory), appraisal (RoB 2, ROBINS-I and JBI item lists with the GRADE domain prompts) and reviewer (the PRISMA 2020 checklist plus a claims-to-source audit). It builds the master CSV schema, pins an R environment in the sandbox with metafor, meta and bayesmeta, and sets up the Project folders: protocol, searches, screening, extraction, analysis, manuscript, gate packages. The dry run re-extracts five studies already verified in the research document and must reproduce their numbers. Hand-over: skills, schema, environment manifest, dry-run report.

**Stage 2, protocol and registration (weeks 3 to 4).** The head agent drafts the protocol in Claude Docs; the statistician agent drafts the synthesis section with the three methods and the declared priors; the citation agent verifies every protocol reference; the reviewer agent audits the protocol against the PRISMA-P items. Database search strings are written per database and tested for recall against the studies already known. Hand-over: protocol, search strings with test-recall results, OSF text, journal shortlist with AI-policy excerpts.

**Stage 3, search and screening (weeks 5 to 8).** Search agents run in parallel, one per database or domain, and write dated record exports. Database exports that need institutional access are run by Sean on his computer and staged into the session. Two screening agents work blind to each other; the head agent computes agreement and lists disagreements for Sean. Hand-over: PRISMA flow counts, agreement statistics, included-study list, full-text PDFs in the Project.

**Stage 4, extraction and appraisal (weeks 8 to 11).** Two extraction agents fill the master CSV independently; the head agent diffs the two and routes conflicts to Sean. The appraisal agent completes RoB 2, ROBINS-I or JBI for each study and drafts the GRADE domain judgments with the reason for each. The citation agent confirms the bibliographic record of every included study. Hand-over: reconciled CSV, discrepancy report, appraisal tables, draft GRADE domains.

**Stage 5, analysis plan (weeks 11 to 12).** The statistician agent writes the statistical analysis plan and the code, runs the code on a synthetic dataset with the real structure, and produces template figures. The reviewer agent checks the plan against the registered protocol and flags any drift. Hand-over: plan, code, synthetic-run outputs, drift report.

**Stage 6, results (weeks 13 to 15).** The statistician agent runs all three methods on the reconciled CSV, produces the Summary of Findings tables, forest, funnel and posterior plots, and the deviations log. The reviewer agent reruns the analysis from the raw file in a fresh session and compares every number. Hand-over: results package, rerun comparison, deviations log.

**Stage 7, manuscript (weeks 16 to 18).** The writer agent drafts to the target journal's format with the PRISMA checklist cross-referenced; the citation agent verifies every reference a final time; the reviewer agent audits every sentence that states a number against the results package. Human authors edit in Claude Docs; the AI-use statement describes exactly which stages used which agents. Hand-over: manuscript, checklist, release package, cover letter.

**Throughout.** The monitor task, once approved at Gate 1, runs weekly: it reruns the registered search terms for new records, checks that every DOI in the master list still resolves, and posts a digest to the Project. Gate packages are stored in the Project under gate-packages with the gate number and date in the file name.

## Quality controls

Six controls run at every stage; each exists because the evidence review in this session hit the failure it guards against.

- **Dual independent work with blinding.** Screening and extraction are done twice by agents that cannot see each other's output; agreement is reported as κ or a discrepancy rate, and every conflict is adjudicated by Sean. A single agent's extraction is never final.
- **Claims-to-source audit.** The reviewer agent takes every number and quotation in a gate package and checks it against the cited page; what it cannot open is listed as unverified, never assumed. In this session the audit caught a wrong journal, a wrong year, a mislabelled guideline grade and a responder rate that was really a percentile.
- **Citation verification with pacing.** Crossref, OpenAlex and publisher pages are queried a few at a time with waits between batches, because all three rate-limited within minutes when hit in bursts; PubMed pages return no content to the fetch tool and are never used as a source. Each reference stores which route confirmed it.
- **Provenance on every datum.** The master CSV has mandatory fields for DOI or URL, location in the source, extractor, date and verification route; the analysis code refuses rows with empty provenance.
- **Fresh-session reruns.** Results are rerun by a reviewer agent that starts without the drafting context; a number that does not reproduce is a gate failure.
- **Human sign-off where journals demand it.** The GRADE table, the analysis plan and the manuscript carry a named human signature; Claude's contribution is logged for the AI-use statement.

**Known tool limits recorded for the plan.** Automated safety filters stopped two agent runs in this session when the work touched immune-challenge studies; the plan routes that extraction through the main session with Sean present rather than through background agents, and keeps the wording clinical. Publisher sites that blocked access (ahajournals, Wiley, Taylor & Francis, Science) are listed so that Sean can retrieve those papers through institutional access and stage them.

## Risks and mitigations

The risks that can sink a journal submission are listed first; each has an owner and the gate at which it is checked.

| Risk | Effect if it happens | Mitigation | Checked at |
| --- | --- | --- | --- |
| Journal rejects the AI-assisted workflow | Desk rejection or retraction | Target journals' AI policies read at G2 and G7; AI-use statement written to the strictest of them; human authors own every section | G2, G7 |
| Agent fabricates or misreads a number | A wrong value reaches a table | Dual extraction, provenance fields, claims-to-source audit, fresh-session rerun | G4, G6 |
| Too few studies to pool for most abilities | Frequentist pooling impossible for k < 3 | Bayesian method with declared priors reports every ability; individual-study intervals shown where k < 3; the limitation stated up front | G5, G6 |
| Best-case reporting inflates the strength ranking | Headline correlation overstated | Sensitivity analysis excluding n ≤ 3 studies; group means versus best cases reported side by side (hypothesis H7 in the research document) | G5, G6 |
| Search recall is poor because database access is limited | Missed studies, reviewer criticism | Institutional database exports run by Sean and staged; recall tested against the studies already known; librarian check of strings | G2, G3 |
| Publisher access blocks | Unverified numbers | Sean retrieves blocked papers through institutional access; nothing unverified enters a table | G3, G4 |
| Tool rate limits or safety filters stop an agent | Stage delay | Paced batches; immune-related extraction done in the main session; stage buffers of one week in the roadmap | all |
| Scope creep into the primary study before the review is done | Both products late | G8 holds the primary study until the review's results are in | G8 |
| Pre-registration drift | Reviewers reject post-hoc choices | Deviations log with dates and reasons; reviewer agent checks the plan against the registration at G5 and G6 | G5, G6 |
| Statistical choices questioned by reviewers | Major revision | Statistician co-author signs the plan; three methods reported with their agreement or disagreement | G5, G7 |

## Decisions needed at Gate 0

Six decisions open Gate 1; each is a tick-box Sean can answer in place or in a comment.

- [ ] Scope of the review: all 26 abilities in the research document, or the lever-free effectors only, with the rest as a secondary table.
- [ ] Target journal tier for the review (a general medical or physiology journal versus a specialist psychophysiology journal), which fixes the AI policy and format the writer follows.
- [ ] Human co-authors: who the statistician and subject-matter co-authors are, or whether to recruit them before Gate 2.
- [ ] Database access: whether Sean has institutional access to Embase, PsycINFO and Web of Science, or the review registers PubMed, Scopus and Google Scholar only.
- [ ] Approval of the monitor as a scheduled weekly task once Gate 1 passes, and of multi-agent workflows for screening and extraction at Gate 3 and Gate 4.
- [ ] Priors for the Bayesian method: accept the weakly informative defaults in Section 4 or ask the statistician co-author to set them.

When all six are answered, Sean sets Gate 0 to Approved and Stage 1 begins.
