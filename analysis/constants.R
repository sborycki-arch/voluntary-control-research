# Shared constants for the VCR Stage 1 analysis scripts. Sourced by 01..04.
# Every value below marked "placeholder pending the statistician co-author's decision at Gate 5" is a Gate 0 / build
# default and is NOT a locked analysis-plan value. Change it here only; no script re-declares it.

# --- Within-person designs (SMCR; register R-069, contract item 3) -------------------------------------------------
# Pre/post correlation used when master_extraction.csv has pre_post_r blank for a pre_post or crossover row.
# Placeholder pending the statistician co-author's decision at Gate 5.
R_PREPOST_DEFAULT <- 0.5
# Sensitivity values re-run by 02_frequentist.R for every SMCR pooling unit (freq_prepost_sensitivity.csv).
# Placeholder pending the statistician co-author's decision at Gate 5.
R_PREPOST_SENS <- c(0.3, 0.7)

# --- Posterior-probability thresholds on the SMD scale (charter D6; reporting/METHODS_PAPER_OUTCOMES) -------------
# "Small" and "moderate" effect thresholds used for P(mu > t) in 03_bayesian.R. Placeholder pending the statistician
# co-author's decision at Gate 5 (the charter carries them as plan defaults).
SMD_THRESHOLD_SMALL <- 0.2
SMD_THRESHOLD_MODERATE <- 0.5

# --- Bayesian priors (charter decision 6: plan defaults stand until the statistician co-author sets them; locked at
# Gate 5). All on the SMD scale; applied only to measures in BAYES_SMD_MEASURES. Placeholder pending Gate 5.
PRIOR_MU_MEAN <- 0
PRIOR_MU_SD <- 1          # mu ~ Normal(0, 1)
PRIOR_TAU_SCALE <- 0.5    # tau ~ half-Normal(0, 0.5)
# Alternative priors reported as sensitivity (mu_mean_wider, mu_mean_tighter in bayes_pooled.csv).
ALT_PRIORS <- list(
  wider   = list(mu_mean = 0, mu_sd = 2,   tau_scale = 1),
  tighter = list(mu_mean = 0, mu_sd = 0.5, tau_scale = 0.25)
)

# --- Measures and routing -------------------------------------------------------------------------------------------
# Measures that are on (or treated as on) the standardised-mean-difference scale and may enter the SMD-scale priors.
BAYES_SMD_MEASURES <- c("SMD", "SMCR", "Z")
# Measures that need their own Bayesian model (Beta-binomial / logit); deferred to Gate 5 by contract item 5.
BAYES_DEFERRED_MEASURES <- c("PLO", "OR")
BAYES_DEFERRED_NOTE <- "Beta-binomial / logit model: Gate 5"

# --- Pooling rules (charter D1; contract item 4) ---------------------------------------------------------------------
K_MIN_POOL <- 3           # pool at k >= 3; below that individual intervals only
K_MIN_EGGER <- 10         # Egger regression test and funnel plot at k >= 10
K_MIN_SUBGROUP_LEVEL <- 2 # lever_type subgroup analysis needs >= 2 levels each with k >= 2
N_SMALL_STUDY <- 3        # sensitivity: exclude rows with n_i <= 3

# --- Controlled vocabularies (SCHEMA.md; validated by 00_load.R, register R-018) -----------------------------------
VOCAB <- list(
  design = c("rct", "crossover", "nonrandomised_comparison", "pre_post", "case_report", "case_series",
             "prevalence_survey", "other"),
  lever_type = c("feedback", "breathing", "muscle", "imagery", "suggestion", "none", "mixed", "unclear"),
  value_source = c("text", "table", "figure", "supplement", "derived"),
  verification_route = c("pdf_full_text", "html_full_text", "supplement", "abstract_only", "not_opened"),
  stat_type = c("mean", "median", "mean_change", "percent", "count", "max_individual", "other"),
  dispersion_type = c("SD", "SE", "CI95", "IQR", "range", "none"),
  is_primary_outcome = c("yes", "no")
)
# condition_label admits free text (the printed label) in addition to intervention/control/baseline/sham: not validated
# against a list, only required to be non-blank.
DESIGNS_INDEPENDENT <- c("rct", "nonrandomised_comparison")
DESIGNS_WITHIN <- c("pre_post", "crossover")
PROVISIONAL_ROUTES <- c("abstract_only", "not_opened")

# --- Output column sets (contract items 2 and 5; order is exact) -----------------------------------------------------
COLS_EFFECT_SIZES <- c("es_id", "study_id", "ability_id", "outcome_measure", "timepoint", "design", "lever_type",
                       "measure", "yi", "vi", "n_i", "n_c", "is_primary_outcome", "synthetic", "derivation")
COLS_FREQ_POOLED <- c("ability_id", "measure", "outcome_measure", "k", "est", "ci_lb", "ci_ub", "pi_lb", "pi_ub",
                      "tau2", "I2", "p", "note")
COLS_FREQ_INDIVIDUAL <- c("es_id", "study_id", "ability_id", "measure", "outcome_measure", "yi", "ci_lb", "ci_ub",
                          "k_ability", "est_natural", "ci_lb_natural", "ci_ub_natural")
COLS_BAYES_POOLED <- c("ability_id", "measure", "k", "mu_mean", "mu_lb", "mu_ub", "tau_median", "p_mu_gt_0.2",
                       "p_mu_gt_0.5", "pred_lb", "pred_ub", "bf_10", "mu_mean_wider", "mu_mean_tighter", "note")
COLS_SOF <- c("ability_id", "outcome", "measure", "k", "source", "study_id", "est", "ci_lb", "ci_ub", "pi_lb", "pi_ub",
              "mu_mean", "mu_lb", "mu_ub", "p_mu_gt_0.2", "p_mu_gt_0.5", "n_studies", "n_participants",
              "final_certainty", "reasons", "plain_language_statement", "note")

OUT_DIR <- "analysis/outputs"

# Working-directory check shared by every script: all paths are relative to the package root.
vcr_check_wd <- function() {
  if (!file.exists("analysis/00_load.R"))
    stop("Run the analysis from the package root (the directory that contains analysis/00_load.R). ",
         "Current working directory: ", getwd(), call. = FALSE)
}
