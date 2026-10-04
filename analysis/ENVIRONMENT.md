# Analysis environment

The build sandbox had no R and no CRAN access, so nothing here is pinned or tested yet. Pinning happens in Claude Code at the dry run:

1. `Rscript analysis/setup.R` — installs renv and the packages, then snapshots.
2. Commit `analysis/renv.lock` and `analysis/session_info.txt` (written by setup.R).
3. Every later run starts with `renv::restore()`; the reviewer's fresh-session rerun uses the same lockfile.

Packages: metafor and meta (frequentist pooling, REML, Hartung-Knapp), bayesmeta (Bayesian normal-normal hierarchical model with closed-form marginals; no Stan needed), brms (alternative Bayesian fit for the prevalence Beta-binomial model, requires a Stan toolchain), dplyr, readr, jsonlite, ggplot2, digest. If brms cannot be installed on the machine, the prevalence model is fitted with metafor's rma.glmm and bayesmeta's logit-scale model and the limitation is logged.

Python is used only for the trace logger (standard library).
