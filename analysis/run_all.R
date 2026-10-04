# run_all.R: one-command rebuild of every table and figure from the master file (VCR_MASTER). Run from the package root:
#   Rscript analysis/run_all.R
# Order: working-directory check; renv::load("analysis") if analysis/renv.lock exists (else the system library is used
# and said so; register R-076); clear analysis/outputs/ except .gitkeep (R-072, R-017); source 00..04; write
# analysis/outputs/MANIFEST.sha256 listing CSV files first, then PNG files, never itself (R-072).
# Figures are compared across machines by the data behind them (freq_loo.csv, freq_individual.csv, effect_sizes.csv),
# not by PNG bytes; the PNG hashes are recorded for completeness only (analysis/ENVIRONMENT.md).
t0 <- Sys.time()
if (!file.exists("analysis/00_load.R"))
  stop("Run the analysis from the package root (the directory that contains analysis/00_load.R). Current working directory: ", getwd(), call. = FALSE)
if (file.exists("analysis/renv.lock") && Sys.getenv("VCR_IGNORE_RENV", "") == "") {
  tryCatch(renv::load("analysis"), error = function(e)
    stop("analysis/renv.lock exists but renv::load('analysis') failed: ", conditionMessage(e),
         "\nRestore the pinned library on a CRAN-reachable machine (renv::restore(project = 'analysis')), or set VCR_IGNORE_RENV=1 ",
         "to run against the system library (the run is then not the pinned environment; say so in the report).", call. = FALSE))
  missing_pkgs <- Filter(function(p) !requireNamespace(p, quietly = TRUE), c("metafor", "dplyr", "readr", "digest"))
  if (length(missing_pkgs))
    stop("analysis/renv.lock loaded but the pinned library lacks ", paste(missing_pkgs, collapse = ", "),
         ": run renv::restore(project = 'analysis') on a CRAN-reachable machine first (or set VCR_IGNORE_RENV=1 to use the system library).", call. = FALSE)
  message("renv: loaded analysis/renv.lock; library paths: ", paste(.libPaths(), collapse = ", "))
} else message(if (file.exists("analysis/renv.lock")) "system library (VCR_IGNORE_RENV set; analysis/renv.lock ignored); R " else "system library (no analysis/renv.lock); R ",
               getRversion(), ", metafor ", as.character(packageVersion("metafor")))
out_dir <- "analysis/outputs"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
stale <- setdiff(list.files(out_dir, all.files = TRUE, no.. = TRUE), ".gitkeep")
if (length(stale)) { unlink(file.path(out_dir, stale), recursive = TRUE); message(sprintf("Removed %d stale output file(s)", length(stale))) }
for (s in c("analysis/00_load.R", "analysis/01_effect_sizes.R", "analysis/02_frequentist.R", "analysis/03_bayesian.R", "analysis/04_sof.R")) {
  message("== ", s); source(s, local = FALSE)
}
csvs <- sort(list.files(out_dir, pattern = "\\.csv$")); pngs <- sort(list.files(out_dir, pattern = "\\.png$"))
files <- c(csvs, pngs)
lines <- vapply(files, function(f) paste0(digest::digest(file.path(out_dir, f), algo = "sha256", file = TRUE), "  ", f), character(1))
writeLines(lines, file.path(out_dir, "MANIFEST.sha256"))
message(sprintf("Rebuilt %d outputs (%d csv, %d png) from %s in %.1f s; manifest analysis/outputs/MANIFEST.sha256",
                length(files), length(csvs), length(pngs), Sys.getenv("VCR_MASTER", "extraction/master_reconciled.csv"),
                as.numeric(Sys.time() - t0, units = "secs")))
