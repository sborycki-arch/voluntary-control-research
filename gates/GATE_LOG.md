# Gate log

Gate status is kept in one place: the **Stage gates** table of the live Claude Research Team Plan,
https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2. This file holds no status
(decision by Sean Borycki, 2026-10-04). Sean sets the Approval dropdown; Claude never sets it.

Claude Code sessions read that table with the docs connector before doing any work (CLAUDE.md, gate rule).
If it cannot be read, the gate counts as not Approved.

The answers to the Gate 0 decisions are recorded in `G0_2026-10-03_charter-decisions.md`
(on branch `stage1-package` until the Stage 1 package is merged).

## Gate packages
Each package has four parts: deliverable, verification note (what was checked and how), adversarial reviewer report, open questions. Store packages under `gates/packages/G<n>-<YYYY-MM-DD>/`. The Stage 1 package uses `gate-packages/G<n>_<date>_<title>.md`; one convention is chosen before that package is merged.
