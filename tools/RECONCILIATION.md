# Reconciliation of the two extractor files

How extractor A's and extractor B's rows become `extraction/master_reconciled.csv`, the only file `analysis/00_load.R` reads. Tool: `tools/reconcile.py` (Python 3 standard library, no installs). File layouts are also in `schema/SCHEMA.md` (Reconciliation files).

## Roles
- Extractors A and B (agents, `skills/extraction/SKILL.md`) each write a complete file in the `schema/master_extraction.csv` layout, blind to each other.
- The head agent runs the diff, hands the discrepancy list to Sean, runs the build, and records every step in the trace (role `head`, inputs = the two extractor files and the log, output = the reconciled file).
- Sean adjudicates every discrepancy in `adjudication_log.csv`. Agents never fill the log.
- The statistician co-author spot-checks the reconciled file (reporting/METHODS_PAPER_OUTCOMES.md #4).

## Procedure
1. Collect the two files, e.g. `extraction/master_A.csv` and `extraction/master_B.csv`. Both must carry the five key fields `study_id, ability_id, outcome_measure, condition_label, timepoint`, unique per row within a file (the tool refuses duplicates and names the lines).
2. Diff: `python3 tools/reconcile.py diff extraction/master_A.csv extraction/master_B.csv --out extraction/discrepancies.csv`. The tool prints the row counts and the count per discrepancy type. The discrepancy ids (`D-0001`…) are assigned in sorted key order and are stable as long as the two input files do not change; if either file is edited, re-run the diff and re-check the log.
3. Sean fills `extraction/adjudication_log.csv`, one row per discrepancy id (schema below). `decision = A` or `B` takes that extractor's value; `other` takes `chosen_value` (for example the value re-read from the paper when both extractors were wrong). For a whole-row discrepancy (`field = row`) the decision is `A` or `B` only: choosing the file in which the row is present keeps it, choosing the other file drops it.
4. Build: `python3 tools/reconcile.py build extraction/master_A.csv extraction/master_B.csv extraction/adjudication_log.csv --primary extraction/primary_outcomes.csv --out extraction/master_reconciled.csv [--date YYYY-MM-DD]`. The tool recomputes the discrepancies, checks the log, and refuses to write anything (exit 2) while any discrepancy lacks a log row, while the log names an id that is not a discrepancy of these files, or while a log row is malformed. Each problem is one line on stderr.
5. Keep A, B, discrepancies.csv, adjudication_log.csv and primary_outcomes.csv next to master_reconciled.csv; they are part of the Gate 7 release and the methods-paper source for outcome #4 (field-level exact-agreement rate = 1 − discrepancies / compared cells; numeric discrepancy rate = `numeric` rows / compared numeric cells; discrepancies by type from the `type` column, with Sean's `reason` giving the misread/wrong-row/unit/omission category).
6. Run `Rscript analysis/00_load.R` (or `run_all.R`) from the package root. The loader refuses rows with blank provenance, out-of-vocabulary values or provisional verification routes, and refuses rows whose `is_primary_outcome` is blank or outside {yes, no} (fail-closed), so a master built without `--primary` does not load.

## What is compared
- All master columns except the key fields and the run-metadata fields. Values are compared after trimming whitespace. Two numeric strings that are numerically equal (`1` and `1.0`) are not a discrepancy; the reconciled file keeps A's printed form.
- Types: `missing_in_A` / `missing_in_B` (one extractor has a value, the other a blank; or, with `field = row`, the whole row exists in one file only), `numeric` (both numeric and different), `text` (any other difference), `provenance` (any difference in source_doi, source_url, location, verbatim_anchor or verification_route, whatever its form, so that provenance conflicts are adjudicated as such and never auto-merged).
- Not compared: `extractor_id`, `extraction_date`, `skill_version`, `model`. They describe the run, not the paper, and always differ between A and B. In the reconciled file `extractor_id = reconciled`, `extraction_date` = the build date, and `skill_version` / `model` are the common value or `A=<a>;B=<b>`.

## adjudication_log.csv
| Column | Content |
|---|---|
| discrepancy_id | id from discrepancies.csv (`D-0001`) |
| decision | `A`, `B` or `other` |
| chosen_value | the value to write when decision is `other` (required then; ignored otherwise) |
| adjudicator | who decided (`sean`, or `human-<initials>` if delegated) |
| date | ISO date |
| reason | one sentence; for methods-paper outcome #4 use the vocabulary misread, wrong row, unit, omission, source ambiguity, other |

## is_primary_outcome
`--primary extraction/primary_outcomes.csv` (columns `study_id, ability_id, outcome_measure`) names the one primary outcome per study × ability, chosen by the head agent from the pre-specified outcome hierarchy of the protocol (Gate 2) and recorded before the build. Every reconciled row whose study_id, ability_id and outcome_measure match an entry gets `yes` (all conditions and timepoints of that outcome); all other rows get `no`. A study × ability with no entry, or an entry matching no row, is reported as a warning. Without `--primary` the column is left blank on every row with a warning; analysis/00_load.R then refuses every row (blank is outside {yes, no}), so the primary-outcome file is required before any analysis (contract items 1 and 4).

## Human-subset comparison (charter D4)
The co-author's blind extraction of the seeded 10–20% subset (`extractor_id = human-<initials>`) is compared with the same tool: `python3 tools/reconcile.py diff extraction/master_reconciled.csv extraction/human_subset.csv --out extraction/discrepancies_human.csv` restricted by the head agent to the subset studies. Its per-type counts give the agent-vs-human field-level agreement and numeric discrepancy rate for reporting/METHODS_PAPER_OUTCOMES.md #4. The human rows are not merged into master_reconciled.csv unless Sean's log says so.

## Feeding 00_load.R
`analysis/00_load.R` reads `extraction/master_reconciled.csv` (override with `VCR_MASTER`), requires the columns listed in its `required_cols`, refuses blank provenance (`source_doi` or `source_url`, `location`, `verbatim_anchor`, `extractor_id`, `extraction_date`, `verification_route`, plus `skill_version` and `model`), refuses out-of-vocabulary values and `pre_post_r` outside [−1, 1], stops on provisional rows, and refuses rows whose `is_primary_outcome` is blank. `reconcile.py build` writes every column the loader requires; a refused row is therefore an extraction or adjudication problem, not a tool problem, and goes back to step 3.
