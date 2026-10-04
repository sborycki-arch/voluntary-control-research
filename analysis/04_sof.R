# 04_sof.R: Summary of Findings table. Joins the pooled (or, below K_MIN_POOL, individual) estimates and the Bayesian
# summaries to the signed GRADE ratings on ability_id + outcome (grade_final.outcome equals the primary row's
# outcome_measure; contract item 6; register R-012 join part, R-075). Env var VCR_GRADE_FINAL (default
# reporting/grade_final.csv). When the GRADE file is absent the table is still written with empty GRADE columns and a
# note. dplyr::any_of is used throughout so a missing column never halts the script.
suppressPackageStartupMessages({library(dplyr); library(readr)})
if (!exists("vcr_loaded")) source("analysis/00_load.R")
source("analysis/constants.R")

rd <- function(f) read_csv(file.path(OUT_DIR, f), show_col_types = FALSE, col_types = cols(.default = "c"))
freq <- rd("freq_pooled.csv") %>% mutate(across(any_of(c("k", "est", "ci_lb", "ci_ub", "pi_lb", "pi_ub")), as.numeric))
indiv <- rd("freq_individual.csv") %>% mutate(across(any_of(c("yi", "ci_lb", "ci_ub", "k_ability")), as.numeric))
bay <- rd("bayes_pooled.csv") %>% mutate(across(any_of(c("mu_mean", "mu_lb", "mu_ub", "p_mu_gt_0.2", "p_mu_gt_0.5")), as.numeric))
es <- rd("effect_sizes.csv")
grade_path <- Sys.getenv("VCR_GRADE_FINAL", "reporting/grade_final.csv")
grade_cols <- c("ability_id", "outcome", "n_studies", "n_participants", "final_certainty", "reasons", "plain_language_statement")

# Estimate rows: pooled units keep the pooled row; units below K_MIN_POOL expand to one row per primary effect size.
pooled_rows <- freq %>% filter(!is.na(est)) %>% mutate(source = "pooled", study_id = NA_character_) %>%
  select(any_of(c("ability_id", "measure", "outcome_measure", "k", "source", "study_id", "est", "ci_lb", "ci_ub", "pi_lb", "pi_ub", "note")))
unpooled_units <- freq %>% filter(is.na(est)) %>% select(any_of(c("ability_id", "measure", "k", "note")))
indiv_rows <- indiv %>% semi_join(es %>% filter(is_primary_outcome == "yes") %>% select(es_id), by = "es_id") %>%
  inner_join(unpooled_units, by = c("ability_id", "measure")) %>%
  mutate(source = "individual", est = yi, pi_lb = NA_real_, pi_ub = NA_real_) %>%
  select(any_of(c("ability_id", "measure", "outcome_measure", "k", "source", "study_id", "est", "ci_lb", "ci_ub", "pi_lb", "pi_ub", "note")))
est_rows <- bind_rows(pooled_rows, indiv_rows) %>% rename(outcome = outcome_measure) %>%
  left_join(bay %>% select(any_of(c("ability_id", "measure", "mu_mean", "mu_lb", "mu_ub", "p_mu_gt_0.2", "p_mu_gt_0.5", "note"))) %>% rename(bayes_note = note),
            by = c("ability_id", "measure")) %>%
  mutate(note = as.character(ifelse(is.na(bayes_note), note, paste0(note, "; bayes: ", bayes_note)))) %>% select(-bayes_note)
# note is forced to character so a zero-row est_rows (no effect sizes) still binds with unmatched GRADE rows.

if (file.exists(grade_path)) {
  grade <- read_csv(grade_path, show_col_types = FALSE, col_types = cols(.default = "c")) %>% select(any_of(grade_cols))
  for (gc in setdiff(grade_cols, names(grade))) grade[[gc]] <- NA_character_
  if (!"signed" %in% names(read_csv(grade_path, show_col_types = FALSE, col_types = cols(.default = "c"), n_max = 0))) message("grade_final has no `signed` column")
  sof <- est_rows %>% left_join(grade, by = c("ability_id", "outcome")) %>%
    mutate(note = as.character(ifelse(is.na(final_certainty), paste0(note, "; no grade_final row for this ability_id + outcome"), note)))
  unmatched <- grade %>% anti_join(est_rows, by = c("ability_id", "outcome"))
  if (nrow(unmatched)) sof <- bind_rows(sof, unmatched %>% mutate(note = "grade_final row without a matching estimate (ability_id + outcome)"))
  grade_note <- sprintf("GRADE from %s", grade_path)
} else {
  sof <- est_rows
  for (gc in setdiff(grade_cols, names(sof))) sof[[gc]] <- NA_character_
  sof$note <- paste0(sof$note, sprintf("; GRADE columns empty: %s not found (set VCR_GRADE_FINAL)", grade_path))
  grade_note <- sprintf("GRADE file %s absent; GRADE columns empty", grade_path)
}
for (cc in setdiff(COLS_SOF, names(sof))) sof[[cc]] <- NA
sof <- sof %>% select(all_of(COLS_SOF)) %>% arrange(ability_id, measure, source, study_id)
write_csv(sof, file.path(OUT_DIR, "summary_of_findings.csv"), na = "NA")
message(sprintf("Summary of Findings: %d rows (%d pooled, %d individual); %s", nrow(sof), sum(sof$source == "pooled", na.rm = TRUE), sum(sof$source == "individual", na.rm = TRUE), grade_note))
