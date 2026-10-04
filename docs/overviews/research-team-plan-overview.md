# Claude Research Team Plan — overview

Compiled 2026-10-03. Full plan (team architecture diagram, the three certainty methods, gate tracker with approval dropdowns, roadmap, work plan, quality controls, risks, Gate 0 decisions): https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2

Companion documents:
- Voluntary Body Control Research Project (evidence base, protocol, 98 references): https://claude.ai/code/artifact/6f9aa87b-3c23-4c5a-a2bf-3b7b0440a3eb
- Voluntary Control Terrain (3D evidence map): https://claude.ai/artifact/HDVbejcMxEMmH8LBqoiEci

## Rule
Ten stage gates (G0 charter, G1 tooling, G1b positive-control reproduction, G2 protocol ... G7 manuscript, G8 primary-study go/no-go). Sean is the sole approver; a stage starts only when its gate is set to Approved in the tracker. Claude never submits, registers, contacts, spends, or starts workflows/scheduled tasks without an approved stage naming it.

## Team (Claude tools)
Head agent (main session + Agent tool) coordinating: parallel search agents; two independent screening agents; two independent extraction agents; appraisal agent (RoB 2 / ROBINS-I / JBI -> GRADE); statistician agent (R: metafor, meta, bayesmeta/brms); adversarial reviewer (fresh session, claims-to-source audit, PRISMA checklist); citation-verification agent (Crossref/OpenAlex/publisher, paced); writer agent (Claude Docs); weekly monitor (scheduled task after G1). Human co-authors required: statistician and subject-matter expert.

## The three certainty methods
1. GRADE certainty per outcome, built on RoB 2 / ROBINS-I / JBI; Summary of Findings tables; PRISMA 2020.
2. Frequentist random-effects meta-analysis: Hedges' g / log OR / logit prevalence, REML tau^2, Hartung-Knapp CIs, prediction intervals, I^2, Egger (k >= 10), leave-one-out; pooling only at k >= 3.
3. Bayesian hierarchical meta-analysis: mu ~ N(0,1), tau ~ half-N(0,0.5) declared in advance, posterior P(mu > 0.2), P(mu > 0.5), posterior predictive, Bayes factor, prior sensitivity; Beta-binomial for prevalence; reported to BARG.

## Timeline
18 weeks: tooling (1-2), protocol & registration (3-4) with the positive-control reproduction alongside, search & screening (5-8), extraction & appraisal (8-11), analysis-plan lock (11-12), results (13-15), manuscript (16-18).

## Gate 0 decisions pending
Scope (all 26 abilities vs lever-free only); target journal tier; human co-authors; database access; approval of the monitor task and workflows; Bayesian priors (defaults vs statistician-set).
