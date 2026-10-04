# setup.R: pin the analysis environment with renv on a CRAN-reachable machine (route 1 in analysis/ENVIRONMENT.md).
# Run once from the package root: Rscript analysis/setup.R. Writes analysis/renv.lock and analysis/session_info.txt.
# Register R-015 (snapshot type "all", sessionInfo after loading the packages), R-067 (`meta` is not installed: no script
# uses it), R-076 (brms failure is logged to ENVIRONMENT.md and does not stop the pin).
if (!file.exists("analysis/00_load.R"))
  stop("Run from the package root (the directory that contains analysis/00_load.R). Current working directory: ", getwd(), call. = FALSE)
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv", repos = "https://cloud.r-project.org")
renv::init(project = "analysis", bare = TRUE, restart = FALSE)
core <- c("metafor", "bayesmeta", "dplyr", "readr", "jsonlite", "ggplot2", "digest")   # `meta` deliberately absent (R-067)
renv::install(core)
# brms needs a Stan toolchain; a failure is recorded and the pin continues (03_bayesian.R does not need brms).
brms_ok <- tryCatch({ renv::install("brms"); TRUE }, error = function(e) {
  cat(sprintf("\n- %s brms not installed: %s\n", format(Sys.Date()), conditionMessage(e)), file = "analysis/ENVIRONMENT.md", append = TRUE)
  message("brms not installed: ", conditionMessage(e)); FALSE })
renv::snapshot(project = "analysis", type = "all", prompt = FALSE)   # "all": every installed package, not only those a script references
# Load every installed analysis package so sessionInfo() carries their versions.
for (p in c(core, if (brms_ok) "brms", "renv")) if (requireNamespace(p, quietly = TRUE)) suppressPackageStartupMessages(library(p, character.only = TRUE))
writeLines(capture.output(sessionInfo()), "analysis/session_info.txt")
message("Wrote analysis/renv.lock and analysis/session_info.txt; run_all.R will renv::load('analysis') on the next run")
