# Handoff

Where the programme stands at the end of a session and what the next session does first. Newest session on top. Gate status is never recorded here: read the live tracker.

## Session of 4 October 2026

### Start here
1. Read the **Stage gates** table of the [live plan](https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2) with the docs connector (CLAUDE.md, gate rule). It is the only gate tracker; this repository holds no gate status.
2. The Stage 1 package is on branch `stage1-package`, not merged into `main`. Its `OPEN_DECISIONS.md` lists everything waiting on Sean and the co-authors; its `CHANGELOG.md` lists every change by finding id.
3. Each cloud session starts in a new container: R is not installed and CRAN is blocked by the proxy. To rerun the tests on a checkout of `stage1-package`:
   - `apt-get install -y r-base-core r-cran-metafor r-cran-dplyr r-cran-readr r-cran-digest r-cran-jsonlite r-cran-ggplot2 r-cran-renv`
   - `bash analysis/synthetic/run_synthetic_tests.sh` (51 checks passed on 4 October)
   - `python3 traces/test_trace_logger.py` (45 checks passed on 4 October)
4. The independent reviewer starts fresh from its own files on branch `review`: `pm_charter.md` (its role and rules), `issues_register.csv`, `gate1_readiness.md` and the pass reports. Give it the items under "For the reviewer's next round".
5. Copying session transcripts into the repository is refused in Auto mode. Switch the session to Accept edits and approve the command when transcripts are to be pushed.

### Where everything is
| What | Where |
| --- | --- |
| Gate tracker (the only one) | [Live plan](https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2), Stage gates table |
| Research document | [Live document](https://claude.ai/code/artifact/6f9aa87b-3c23-4c5a-a2bf-3b7b0440a3eb); copy at `docs/research-project.md` |
| Stage 1 report (status, reviewer results, open findings) | [Claude Doc, private](https://claude.ai/artifact/LqY1yJhgk9w2kqFFYxiDvr) |
| Stage 1 package and its trace log | Branch `stage1-package` (`traces/stage1.jsonl`, `OPEN_DECISIONS.md`, `CHANGELOG.md`, `build-log/`) |
| Reviewer's files after pass 5 | Branch `review` |
| Platform transcripts, snapshot 16:09 UTC | Branch `transcripts` (`INDEX.md` maps each trace record to its transcript) |
| Plain-language summary of the pilot (not for citation) | `docs/summaries/` |

### Done on 4 October
- Gate 0: Sean set the live tracker; the reviewer read it at revision 13 and closed its blocker (R-043).
- The live plan became the only gate tracker; `gates/GATE_LOG.md` points to it, and the gate rule in `CLAUDE.md` reads it.
- This private repository was created, with `main` as the default branch.
- Stage 1 round-2 fixes: 34 findings closed by the reviewer's own checks in pass 4; 16 major findings remain, none a blocker.
- The research document's lever claim was corrected, live and in `docs/`: seven of the ten High-certainty abilities work through a lever, not all ten.
- New gate G1b, positive-control reproduction: the full pipeline must recover Paravlic et al. 2018's pooled estimate (0.72, 95% CI 0.42 to 1.02). It is in the live plan's tracker, Summary, roadmap and work plan, and in `docs/research-team-plan.md`.

### Waiting on Sean
- Everything in `OPEN_DECISIONS.md` on `stage1-package`. The ones that gate Gate 1: the environment route (R-038); full texts for the dry run (R-029); rulings on R-021, R-068, R-020, R-044, R-045 and R-027; the after-the-fact build record (R-001); the transcript policy (R-007); the repository layout (R-048 to R-050).
- Piloerection: the research document calls it lever-free, but its dataset gives the lever as "Head/neck tension", and hypothesis H3 predicts it will fail the lever-free test.
- G1b, when it opens: Paravlic 2018's list of included studies and their full texts, and line-item approval of the two parallel extractors (charter decision 7).
- The copy of the research overview in the Huberman Lab Claude Project still carries the uncorrected lever claim.

### For the reviewer's next round
- Its two pass-5 questions are answered by Sean's own messages of 4 October: "Live plan only; set up the private repo" and "Drop down should be saved".
- Verify the repository directly: the pointer in `gates/GATE_LOG.md` and the gate rule in `CLAUDE.md` on `main`; the four branches; `INDEX.md` on `transcripts`.
- The lever correction (live document and `docs/`) and the piloerection inconsistency.
- G1b: it covers R-028 (the dry run never pools real data), and the live Summary now says ten gates (R-062).
- Audit the Stage 1 report, which quotes the pass-5 figures.
- Minor builder fixes queued for the next round: R-078, R-080 to R-083 and the R-037 residual.

### Not pushed
- Answers to the two questions Sean marked "inquiry, not for record", and the bell-curve chart that followed them.
- Container-only material: test copies, the R installation, virtual environments.
- The main-session transcript after 16:09 UTC.
