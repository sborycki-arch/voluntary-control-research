# One-command rebuild of every table and figure from the raw file. Writes a SHA-256 manifest of outputs.
t0 <- Sys.time()
if (file.exists("analysis/renv.lock")) renv::restore(project = "analysis", prompt = FALSE)
for (s in c("analysis/00_load.R", "analysis/01_frequentist.R", "analysis/02_bayesian.R", "analysis/03_sof.R")) { message("== ", s); source(s) }
files <- list.files("analysis/outputs", full.names = TRUE)
writeLines(paste(sapply(files, digest::digest, algo = "sha256", file = TRUE), basename(files)), "analysis/outputs/MANIFEST.sha256")
message(sprintf("Rebuilt %d outputs in %.1f s", length(files), as.numeric(Sys.time() - t0, units = "secs")))
