# Summary of Findings table: joins pooled estimates with the signed GRADE ratings.
suppressPackageStartupMessages({library(dplyr); library(readr)})
freq <- read_csv("analysis/outputs/freq_pooled.csv", show_col_types = FALSE)
bay <- read_csv("analysis/outputs/bayes_pooled.csv", show_col_types = FALSE)
grade <- read_csv("reporting/grade_final.csv", show_col_types = FALSE)   # signed by the subject-matter co-author
sof <- grade %>% left_join(freq, by = "ability_id") %>% left_join(bay, by = "ability_id") %>%
  select(ability_id, outcome, n_studies, n_participants, est, ci_lb, ci_ub, pi_lb, pi_ub, mu_mean, mu_lb, mu_ub,
         p_mu_gt_0.2, p_mu_gt_0.5, final_certainty, reasons, plain_language_statement)
write_csv(sof, "analysis/outputs/summary_of_findings.csv")
