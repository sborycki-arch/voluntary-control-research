Sean has uploaded the research bundle you were holding for; it is extracted read-only at /tmp/claude-0/-home-user-chick-contact-system/9737741b-6ce5-5409-92dc-67b8f29eb2a7/scratchpad/inputs (call it INPUTS).

What it contains:
- INPUTS/docs/research-team-plan.md — the Claude Research Team Plan (gates, team architecture, three methods, work plan, quality controls, risks, the six Gate 0 decisions). Sean says the plan for execution is in here.
- INPUTS/docs/research-project.md — the research document: rubrics, evidence by system, quantitative synthesis, Verification status table (Section "Verification status": 72 of 98 sources read in primary; 26 listed with gaps), gaps, proposed protocol, reference list.
- INPUTS/docs/evidence-dataset.md — the evidence map as a ranked table with the population SDs used.
- INPUTS/data/evidence.json, evidence.csv, baselines.csv — scored dataset (26 abilities) and the population baselines.
- INPUTS/analysis/evidence.py — rebuilds evidence.json. The head agent ran it on a copy: rebuilt evidence.json is byte-identical to the shipped one.
- INPUTS/CLAUDE.md — working rules for the research repo (gate rule, provenance, dual extraction, pacing, style for Sean).
- INPUTS/gates/GATE_LOG.md — the repo's gate tracker. Note: it still shows G0 "Awaiting approval" and all six decision boxes unticked, while PKG/gate-packages/G0_2026-10-03_charter-decisions.md records G0 approved 2026-10-03. Only Sean writes Approved; treat the discrepancy as a finding for him, not something to fix.
- INPUTS/skills/README.md — the research repo's placeholder for the four skills (planned layout).
- INPUTS/viz/ — terrain map and token chart; out of scope for the review.

If you have already finished your setup deliverables, start the second pass now. If you are still in the setup run, finish it first (including the trace `end`), then start the second pass. Second pass:
1. Re-review the Stage 1 package (PKG) against the plan: the Stage 1 work-plan paragraph, the G1 row of the gate table (deliverable and acceptance criteria), the team-architecture table, the three-methods section, the quality controls, the known tool limits, and CLAUDE.md's working rules. Record every place the package departs from the plan or the plan departs from the charter record.
2. Check the dry-run candidates in PKG/dry-run/DRY_RUN_PROTOCOL.md against the research document: are the pilot values quoted correctly; does each candidate's source appear in the Verification status table (if it does, it is not "verified" and the protocol's selection rule (a) excludes it); which five candidates actually qualify.
3. Check PKG/schema/population_sd.csv against INPUTS/data/baselines.csv and the research document's baseline table, cell by cell.
4. Check PKG/skills/screening/references/abilities.md (26 abilities, A01–A26) against the 26 rows of INPUTS/data/evidence.csv: same set, same names, same key sources.
5. Repository integration: the research repo has its own layout (gates/packages/G<n>-<date>/, skills/, data/, analysis/) and the package has another (gate-packages/G<n>_<date>_<title>.md, schema/, traces/). State where they conflict and what Sean must decide before the package is merged into the repo. Do not propose a merge yourself.
6. Update issues_register.csv (new rows, source = reviewer-pass2; keep existing ids), gate1_readiness.md and input_request.md (strike what is now supplied; list what is still missing, e.g. the live-document dropdown state, the 98-reference list if it is not in the markdown export, full texts for dry-run studies).
7. Write PM/reviewer_report_G1-prep_pass2_2026-10-04.md in the same format as the first report, with a section "Plan vs charter record" and a section "Open questions for Sean".
8. Log this pass as its own trace: run `start` yourself with role reviewer, instance single, --prompt pointing at a file under PM/prompts/ containing this message verbatim (write it there first), --inputs the INPUTS files you actually read; run `end` when done with --outputs your pass-2 files. Use PKG/traces/trace_logger.py; it writes to PKG/traces/stage1.jsonl, which is the permitted write. Do not run start and end concurrently with any other logger call.

Same rules as before: report, do not fix; nothing under PKG or INPUTS is edited; no connectors, no scheduling, no external posting; no questions mid-run — put them in the report. When done, return as plain data: pass-2 judgment line, counts, new blocker/major ids with one-line titles, the integration decisions Sean must make, and what is still missing.
