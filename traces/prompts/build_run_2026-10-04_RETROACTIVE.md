# Stage 1 build run, 2026-10-04 — RETROACTIVE prompt stand-in

This file is not the prompt the builder agent received. The original prompt of the Stage 1 build run was
not preserved: the build ran before the trace logger existed (the logger is itself one of the build's
outputs) and no prompt file, transcript or trace record was written at the time (register R-001).

This file stands in for `prompt_ref` in the retroactive trace record so that the record has a hashable
prompt reference. The record is marked `retroactive: true`, `model: not_recorded`, `skill_name: not_recorded`.
Whether a retroactive record is acceptable for the Gate 1 package is Sean's decision (reviewer open
question Q12 in reviewer_report_G1-prep_pass2_2026-10-04.md; Q2 in the pass-1 report).

## What is known about the run

- Delivered artefact: `badc0db9-vcr-stage1-build.zip` (upload id badc0db9; 59 members under `vcr/`),
  sha256 `0c3b2b8a6dad61434f5023da8fe84c6932af86987fbbf6bc67f03595e34eded2`.
- Zip member timestamps run from 2026-10-04T03:34:44Z to 2026-10-04T03:41:38Z; the record's
  `started_at` / `ended_at` are set to 2026-10-04T03:34:00Z and 2026-10-04T03:41:00Z from those timestamps
  (rounded down to the minute), not from a clock observed during the run.
- The run was performed by a separate builder agent, not by the head agent that wrote the plan's Stage 1
  skills (pass-2 note on R-001). Its model string and settings were not recorded; the platform's default
  model in this program is claude-fable-5-1, but that is an inference, not a record, so `model` is
  `not_recorded`.
- Inputs: not recorded. The charter `gate-packages/G0_2026-10-03_charter-decisions.md` is inside the
  delivered zip and is the only input that can be named with confidence; it is listed as the record's
  single input_ref.
- Outputs: `README.md` and the `skills/`, `schema/` and `analysis/` files of the delivered package, plus
  the zip itself. The record's `output_refs` point at the read-only reviewer copy
  `scratchpad/vcr/` (verified byte-identical to the zip members, 20 of 20 sha256 matches) rather than at
  the round-2 working copy, because the working copy was already being modified by the round-2 fixers when
  this record was written; the hashes in the record are therefore the hashes of the files as delivered.
- The build also wrote `dry-run/`, `reporting/`, `monitor/`, `gate-packages/` and `traces/` (logger and
  spec); these are in the zip but are not listed individually in `output_refs` (the zip hash covers them).

## Record written by

Fixer A (traces), round-2 build, trace `s1-builder-A-20261004T115625Z-3745`, using the round-2 logger
(`traces/trace_logger.py` as rewritten for R-003/R-077) with `--retroactive`.
