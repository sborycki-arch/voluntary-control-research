# Load the reconciled master file and refuse rows without provenance.
suppressPackageStartupMessages({library(dplyr); library(readr)})
master_path <- Sys.getenv("VCR_MASTER", "extraction/master_reconciled.csv")
m <- read_csv(master_path, show_col_types = FALSE, col_types = cols(.default = "c"))
prov <- c("location", "verbatim_anchor", "extractor_id", "extraction_date", "verification_route")
missing_prov <- m %>% filter(is.na(source_doi) & is.na(source_url) |
                             if_any(all_of(prov), ~ is.na(.x) | .x == ""))
if (nrow(missing_prov) > 0) {
  write_csv(missing_prov, "analysis/outputs/REFUSED_missing_provenance.csv")
  stop(sprintf("%d rows refused for missing provenance; see analysis/outputs/REFUSED_missing_provenance.csv", nrow(missing_prov)))
}
provisional <- m %>% filter(verification_route %in% c("abstract_only", "not_opened"))
if (nrow(provisional) > 0) stop(sprintf("%d rows are provisional (abstract_only/not_opened); resolve before analysis", nrow(provisional)))
pop <- read_csv("schema/population_sd.csv", show_col_types = FALSE, col_types = cols(.default = "c")) %>%
  filter(status == "verified")
num <- c("n_total","n_condition","value","dispersion_value","ci_low","ci_high","baseline_value","baseline_dispersion","n_responders","n_tested")
m <- m %>% mutate(across(all_of(num), ~ suppressWarnings(as.numeric(.x))))
dir.create("analysis/outputs", showWarnings = FALSE, recursive = TRUE)
message(sprintf("Loaded %d rows, %d abilities, %d population-SD rows", nrow(m), n_distinct(m$ability_id), nrow(pop)))
