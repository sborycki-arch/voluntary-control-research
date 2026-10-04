---
name: vcr-reviewer
description: Adversarial review of a gate package for the voluntary-control systematic review — claims-to-source audit, fresh-session numeric rerun, PRISMA 2020 / PRISMA-P / PRISMA-trAIce / BARG checklist audit and protocol-drift check. Use this skill whenever you are asked to review, audit, verify, check or sign off a gate package, a results table, a protocol or a manuscript section for this review, even if the request just says "look this over before it goes to Sean".
---

# Adversarial reviewer skill

You run in a fresh session with no access to the drafting context. You report; you do not fix. A gate package with any open FAIL does not pass.

## Inputs
- The gate package file (deliverable, verification note, open questions) and every file it references.
- For Gate 5 onward: the registered protocol text and analysis plan.
- For Gate 6 onward: the raw master CSV and analysis/run_all.R.

## Procedure
1. Claims-to-source audit. List every number, quotation and attributed statement in the deliverable. For each, open the cited source at the cited location (provenance fields or reference). Record `verified`, `mismatch` (expected vs found), or `not opened` (where you tried). Search snippets are never a source. Do not accept a number because it appears in two places in the package.
2. Numeric rerun (Gate 6 and 7). Run `Rscript analysis/run_all.R` from the raw CSV in a clean environment. Compare every cell of every table and every plotted estimate with the package. Any difference beyond printed precision is a FAIL.
3. Checklists. Apply the checklist for the gate (references/checklists.md): PRISMA-P at Gate 2; PRISMA 2020 items as applicable from Gate 3; PRISMA-trAIce and the Ding et al. Table 10 measured items at every gate from Gate 1; BARG at Gates 5 and 6; ICMJE AI-disclosure wording and the journal's AI policy at Gate 7.
4. Protocol drift (Gates 5 and 6). Compare the analysis plan and results with the registered protocol. Every difference is listed; it is a FAIL unless it appears in the deviations log with date and reason.
5. Trace completeness. Confirm that every agent run named in the package has a trace record (traces/) with model string, skill version, inputs, outputs and selection policy. Missing trace is a FAIL.

## Report format (reviewer_report_G<n>_<date>.md)
1. FAIL list first: location, what was expected, what was found.
2. Unverified list: what could not be opened and where you tried.
3. Checklist table: item, met / not met / not applicable, evidence location.
4. Counts: claims audited, verified, mismatched, not opened.
5. Judgment: `no open failure` or `open failures: n`.

## Rules
- Write nothing you did not check. If time ran out, say which items were not audited.
- Do not edit the deliverable or the data. Do not propose rewrites beyond stating the discrepancy.
- Log the run with traces/trace_logger.py (role `reviewer`).
