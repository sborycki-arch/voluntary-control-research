# 00_load.R: load the reconciled master file, refuse rows without provenance or outside the controlled vocabularies,
# load the population-SD table, and coerce numeric columns. All paths are relative to the package root.
# Env vars: VCR_MASTER (default extraction/master_reconciled.csv), VCR_POPULATION_SD (default schema/population_sd.csv).
suppressPackageStartupMessages({library(dplyr); library(readr)})
if (!file.exists("analysis/00_load.R"))
  stop("Run the analysis from the package root (the directory that contains analysis/00_load.R). ",
       "Current working directory: ", getwd(), call. = FALSE)
source("analysis/constants.R")
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)   # before any write (register R-017)

master_path <- Sys.getenv("VCR_MASTER", "extraction/master_reconciled.csv")
pop_path <- Sys.getenv("VCR_POPULATION_SD", "schema/population_sd.csv")
if (!file.exists(master_path)) stop("Master file not found: ", master_path, " (set VCR_MASTER)", call. = FALSE)
m <- read_csv(master_path, show_col_types = FALSE, col_types = cols(.default = "c"), na = character())
m <- m %>% mutate(across(everything(), ~ trimws(.x)))
m$.row <- seq_len(nrow(m))
blank <- function(x) is.na(x) | x == ""

required_cols <- c("study_id", "ability_id", "design", "n_total", "condition_label", "n_condition", "comparator_label", "lever_type",
                   "outcome_measure", "unit", "timepoint", "stat_type", "value", "dispersion_type", "dispersion_value",
                   "ci_low", "ci_high", "baseline_value", "baseline_dispersion", "n_responders", "n_tested", "pre_post_r",
                   "is_primary_outcome", "value_source", "source_doi", "source_url", "location", "verbatim_anchor",
                   "extractor_id", "extraction_date", "verification_route", "skill_version", "model")
missing_cols <- setdiff(required_cols, names(m))
if (length(missing_cols))
  stop("Master file lacks required columns: ", paste(missing_cols, collapse = ", "), call. = FALSE)

# --- 1. Provenance refusal (SCHEMA.md: source_doi or source_url, location, verbatim_anchor, extractor_id,
#        extraction_date, verification_route) plus non-blank skill_version and model (register R-018). -------------
prov <- c("location", "verbatim_anchor", "extractor_id", "extraction_date", "verification_route", "skill_version", "model")
prov_reason <- function(r) {
  reasons <- character()
  if (blank(r[["source_doi"]]) && blank(r[["source_url"]])) reasons <- c(reasons, "source_doi and source_url both blank")
  for (f in prov) if (blank(r[[f]])) reasons <- c(reasons, paste0(f, " blank"))
  paste(reasons, collapse = "; ")
}
m$reason <- vapply(seq_len(nrow(m)), function(i) prov_reason(m[i, ]), character(1))
missing_prov <- m %>% filter(reason != "")
if (nrow(missing_prov) > 0) {
  write_csv(missing_prov %>% select(-.row), file.path(OUT_DIR, "REFUSED_missing_provenance.csv"))
  stop(sprintf("%d row(s) refused for missing provenance (rows %s); see %s/REFUSED_missing_provenance.csv",
               nrow(missing_prov), paste(missing_prov$.row, collapse = ","), OUT_DIR), call. = FALSE)
}

# --- 2. Controlled-vocabulary refusal (register R-018). condition_label is free text (printed label) and only has
#        to be non-blank. ability_id must be A01..A26, semicolon-separated if more than one. --------------------------
vocab_reason <- function(r) {
  reasons <- character()
  for (f in names(VOCAB)) {
    v <- r[[f]]
    if (blank(v) || !(v %in% VOCAB[[f]])) reasons <- c(reasons, sprintf("%s='%s' not in {%s}", f, v, paste(VOCAB[[f]], collapse = "|")))
  }
  if (blank(r[["condition_label"]])) reasons <- c(reasons, "condition_label blank")
  ab <- strsplit(r[["ability_id"]], ";")[[1]]
  if (blank(r[["ability_id"]]) || !all(grepl("^A(0[1-9]|1[0-9]|2[0-6])$", trimws(ab)))) reasons <- c(reasons, sprintf("ability_id='%s' not A01..A26", r[["ability_id"]]))
  if (!blank(r[["pre_post_r"]])) {
    rr <- suppressWarnings(as.numeric(r[["pre_post_r"]]))
    if (is.na(rr) || rr < -1 || rr > 1) reasons <- c(reasons, sprintf("pre_post_r='%s' not numeric in [-1, 1]", r[["pre_post_r"]]))
  }
  paste(reasons, collapse = "; ")
}
m$reason <- vapply(seq_len(nrow(m)), function(i) vocab_reason(m[i, ]), character(1))
bad_vocab <- m %>% filter(reason != "")
if (nrow(bad_vocab) > 0) {
  write_csv(bad_vocab %>% select(-.row), file.path(OUT_DIR, "REFUSED_vocabulary.csv"))
  stop(sprintf("%d row(s) refused for controlled-vocabulary violations (rows %s); see %s/REFUSED_vocabulary.csv",
               nrow(bad_vocab), paste(bad_vocab$.row, collapse = ","), OUT_DIR), call. = FALSE)
}
m$reason <- NULL

# --- 3. Provisional rows (abstract_only / not_opened) stop the analysis. ---------------------------------------------
provisional <- m %>% filter(verification_route %in% PROVISIONAL_ROUTES)
if (nrow(provisional) > 0)
  stop(sprintf("%d row(s) are provisional (abstract_only/not_opened; rows %s); resolve before analysis",
               nrow(provisional), paste(provisional$.row, collapse = ",")), call. = FALSE)

# --- 4. Exactly one primary outcome per study x ability (contract item 1). -----------------------------------------
prim <- m %>% group_by(study_id, ability_id) %>% summarise(n_yes = sum(is_primary_outcome == "yes"), .groups = "drop") %>% filter(n_yes == 0)
if (nrow(prim) > 0)
  warning(sprintf("%d study x ability combination(s) have no is_primary_outcome = yes row (%s); they will not enter pooling",
                  nrow(prim), paste(paste(prim$study_id, prim$ability_id), collapse = "; ")), call. = FALSE)

# --- 5. Population-SD table: only verified rows are used (SCHEMA.md). ------------------------------------------------
if (file.exists(pop_path)) {
  pop <- read_csv(pop_path, show_col_types = FALSE, col_types = cols(.default = "c"), na = character()) %>%
    mutate(across(everything(), ~ trimws(.x)))
  pop_all_n <- nrow(pop)
  pop <- pop %>% filter(status == "verified") %>%
    mutate(across(c(mean, sd, n), ~ suppressWarnings(as.numeric(.x))))
} else {
  warning("Population-SD file not found: ", pop_path, " (set VCR_POPULATION_SD); no Z effect sizes will be computed", call. = FALSE)
  pop <- tibble(ability_id = character(), variable = character(), mean = numeric(), sd = numeric(), unit = character(),
                population = character(), n = numeric(), status = character())
  pop_all_n <- 0
}

# --- 6. Numeric coercion ----------------------------------------------------------------------------------------------
num <- c("n_total", "n_condition", "value", "dispersion_value", "ci_low", "ci_high", "baseline_value", "baseline_dispersion",
         "n_responders", "n_tested", "pre_post_r")
m <- m %>% mutate(across(all_of(num), ~ suppressWarnings(as.numeric(.x)))) %>% select(-.row)
vcr_loaded <- TRUE
message(sprintf("Loaded %d rows, %d abilities from %s; %d verified population-SD rows (of %d) from %s",
                nrow(m), n_distinct(m$ability_id), master_path, nrow(pop), pop_all_n, pop_path))
