# Analysis environment

All scripts run from the package root (the directory that contains `analysis/00_load.R`); every path is relative to it
and every script stops with a plain message when started elsewhere. One command rebuilds every table and figure:

    Rscript analysis/run_all.R            # VCR_MASTER, VCR_POPULATION_SD, VCR_GRADE_FINAL select the inputs

Inputs: `VCR_MASTER` (default `extraction/master_reconciled.csv`), `VCR_POPULATION_SD` (default `schema/population_sd.csv`;
only `status = verified` rows are used), `VCR_GRADE_FINAL` (default `reporting/grade_final.csv`; when absent the Summary of
Findings is written with empty GRADE columns and a note). Outputs go to `analysis/outputs/` (cleared first, except
`.gitkeep`) with `MANIFEST.sha256` listing the CSV files first, then the PNG files, never itself.

Pipeline: `00_load.R` (provenance and controlled-vocabulary refusal, writes `REFUSED_*.csv` with a `reason` column) →
`01_effect_sizes.R` (SMD / SMCR / PLO / OR / Z from the master file; `effect_sizes.csv`) → `02_frequentist.R` (REML,
Knapp-Hartung, prediction interval, leave-one-out, Egger and funnel at k ≥ 10, sensitivity and pre/post-r sensitivity;
`freq_*.csv`, forest/funnel PNG) → `03_bayesian.R` (bayesmeta, SMD-scale measures only; `bayes_pooled.csv`) →
`04_sof.R` (`summary_of_findings.csv`, joined to GRADE on `ability_id` + `outcome`). Shared constants, including the
placeholder pre/post correlation `R_PREPOST_DEFAULT = 0.5` (placeholder pending the statistician co-author's decision at
Gate 5) and the priors, live in `analysis/constants.R`.

## What is pinned, and how

Nothing is pinned yet (no `analysis/renv.lock` is committed). The pin is a Gate 1 deliverable made on a CRAN-reachable
machine (route 1 below); the environment route itself is Sean's decision (register R-038). Until then every run reports
`system library (no analysis/renv.lock); R <version>, metafor <version>` on its first line, and the versions below are the
record of what the scripts were exercised against.

Package set the scripts load: metafor (escalc, rma, predict, leave1out, regtest, forest, funnel), dplyr, readr, digest
(manifest), jsonlite (trace tooling), ggplot2 (reserved for report figures), bayesmeta (03_bayesian.R only, optional at
run time), renv (route 1 only). `meta` is **not** pinned and not installed: no script uses it (register R-067; the plan's
"metafor, meta and bayesmeta" named it as an alternative implementation of the same REML/HKSJ model, which metafor
provides). brms is optional: the prevalence Beta-binomial model is a Gate 5 decision and 03_bayesian.R does not call it.

## Three admissible routes

1. **renv on a CRAN-reachable machine (the intended pin).** `Rscript analysis/setup.R` runs `renv::init(bare = TRUE)`,
   installs metafor, bayesmeta, dplyr, readr, jsonlite, ggplot2, digest, tries brms inside `tryCatch` (a failure appends a
   dated line `brms not installed: <reason>` to this file and continues), then `renv::snapshot(type = "all")` so every
   installed package reaches `analysis/renv.lock`, loads every installed analysis package and writes
   `analysis/session_info.txt` with their versions. Commit `analysis/renv.lock` and `analysis/session_info.txt`. A fresh
   checkout runs `Rscript -e "renv::restore(project = 'analysis')"` once; `run_all.R` then calls `renv::load("analysis")`
   before anything else, prints the library paths it is using, and stops with a plain message if the lockfile exists but
   the pinned library has not been restored (verified: with an unrestored lockfile the run stops at
   "pinned library lacks metafor, dplyr, readr, digest: run renv::restore ..."; it does not fall back silently).
   `VCR_IGNORE_RENV=1` bypasses the lockfile deliberately and says so on the first line.
2. **System / apt R as present in the build container (what every script was run against on 2026-10-04).**
   R 4.3.3 (2024-02-29), metafor 4.4.0, dplyr 1.1.4, readr 2.1.5, digest 0.6.34, jsonlite 1.8.8, ggplot2 3.4.4,
   renv 1.0.3, brms 2.20.4 (installed from apt, not used); bayesmeta and meta absent (CRAN unreachable, HTTP 403 from
   the proxy). `bash analysis/synthetic/run_synthetic_tests.sh` passes in this configuration (two synthetic masters,
   all contract headers and counts asserted; output pasted in CHANGELOG_B.md).
3. **Python alternative.** The plan's G1 row allows "pinned R or Python environment". No Python analysis code exists;
   if this route is chosen the effect-size conventions in SCHEMA.md and the output column sets in `analysis/constants.R`
   are the specification to reimplement, and `analysis/synthetic/run_synthetic_tests.sh` is the acceptance test to pass
   (its assertions are on the CSV files, not on R). The trace logger and the synthetic-data generator are Python 3
   standard library already.

## bayesmeta absence: what the scripts do without it

`03_bayesian.R` checks `requireNamespace("bayesmeta")`. When it is absent the script writes `bayes_pooled.csv` with the
full contract column set and the note `bayesmeta not installed` on every ability × measure row, emits one R warning, and
returns normally, so `run_all.R` completes and the Summary of Findings carries empty Bayesian columns with that note.
When it is present, only SMD, SMCR and Z units enter the declared SMD-scale priors (Normal(0, 1), half-Normal(0, 0.5),
plus the wider and tighter alternatives in `constants.R`); PLO and OR units receive the note `Beta-binomial / logit
model: Gate 5` and no fit; k = 1 is fitted and noted as prior-dominated; every bayesmeta call is wrapped in `tryCatch`
with the error text written to `note`. The bayesmeta code path has therefore been exercised only as far as the guard and
the note rows in this container; its fits must be run under route 1 before Gate 5 (register R-016, guards only).

## Figures and the manifest

`MANIFEST.sha256` hashes every CSV first, then every PNG. PNG bytes may differ across R builds and graphics devices even
when the analysis is identical, so figures are compared across machines by the data behind them (`effect_sizes.csv`,
`freq_pooled.csv`, `freq_loo.csv`, `freq_individual.csv`), not by PNG hash; a PNG hash difference alone is not a
reproduction failure (register R-072). In this container two consecutive runs on the same master give byte-identical
PNGs.

## Synthetic data

`analysis/synthetic/make_synthetic_master.py` (standard library, seeded) writes two obviously synthetic masters (every
`study_id` starts with `synth_`; provenance fields carry `SYNTHETIC` / `synthetic.invalid` values), one population-SD
file with a single `verified` row, and one `grade_final` file with the contract header. They exercise every effect-size
route, k < 3 (dry-run shape: five abilities, k = 1 each) and k ≥ 3 pooling with Egger/funnel at k = 12. They live under
`analysis/synthetic/` and never under `extraction/`; `effect_sizes.csv` marks their rows `synthetic = yes`.
