# Run once in Claude Code to pin the environment. Writes renv.lock and session_info.txt.
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv", repos = "https://cloud.r-project.org")
renv::init(project = "analysis", bare = TRUE, restart = FALSE)
pkgs <- c("metafor", "meta", "bayesmeta", "brms", "dplyr", "readr", "jsonlite", "ggplot2", "digest")
renv::install(pkgs)
renv::snapshot(project = "analysis", prompt = FALSE)
writeLines(capture.output(sessionInfo()), "analysis/session_info.txt")
