# 03_bayesian.R: Method 3, Bayesian normal-normal hierarchical model (bayesmeta) with the declared priors
# (constants.R; charter D6 plan defaults, placeholder pending the statistician co-author's decision at Gate 5). Reported
# to BARG. Register R-016 (guards), R-070 (scale routing).
# Routing: only measures in BAYES_SMD_MEASURES (SMD, SMCR, Z) enter the SMD-scale priors and the 0.2/0.5 thresholds.
# PLO and OR units get a note row (BAYES_DEFERRED_NOTE) and no fit. k = 1 is allowed (posterior is prior-dominated) and
# noted. Every bayesmeta call is wrapped in tryCatch; errors go to `note`. If bayesmeta is not installed the script
# writes a note row for every ability x measure, warns, and returns normally so run_all.R continues.
suppressPackageStartupMessages({library(dplyr); library(readr)})
if (!exists("vcr_loaded")) source("analysis/00_load.R")
source("analysis/constants.R")

es <- read_csv(file.path(OUT_DIR, "effect_sizes.csv"), show_col_types = FALSE, col_types = cols(.default = "c", yi = "d", vi = "d"))
prim <- es %>% filter(is_primary_outcome == "yes")
units <- prim %>% count(ability_id, measure, name = "k") %>% arrange(ability_id, measure)
na_row <- function(ab, me, k, note) tibble(ability_id = ab, measure = me, k = k, mu_mean = NA_real_, mu_lb = NA_real_, mu_ub = NA_real_,
  tau_median = NA_real_, p_mu_gt_0.2 = NA_real_, p_mu_gt_0.5 = NA_real_, pred_lb = NA_real_, pred_ub = NA_real_, bf_10 = NA_real_,
  mu_mean_wider = NA_real_, mu_mean_tighter = NA_real_, note = note)
have_bayesmeta <- requireNamespace("bayesmeta", quietly = TRUE)
out <- list()
if (!have_bayesmeta) {
  warning("bayesmeta not installed: bayes_pooled.csv carries note rows only (see analysis/ENVIRONMENT.md)", call. = FALSE)
  for (i in seq_len(nrow(units))) out[[i]] <- na_row(units$ability_id[i], units$measure[i], units$k[i], "bayesmeta not installed")
} else {
  suppressPackageStartupMessages(library(bayesmeta))
  tau_prior <- function(scale) function(t) bayesmeta::dhalfnormal(t, scale = scale)
  for (i in seq_len(nrow(units))) {
    ab <- units$ability_id[i]; me <- units$measure[i]; k <- units$k[i]
    d <- prim %>% filter(ability_id == ab, measure == me)
    if (me %in% BAYES_DEFERRED_MEASURES) { out[[i]] <- na_row(ab, me, k, BAYES_DEFERRED_NOTE); next }
    if (!(me %in% BAYES_SMD_MEASURES)) { out[[i]] <- na_row(ab, me, k, sprintf("measure %s has no declared prior", me)); next }
    k_note <- if (k == 1) "k=1: posterior dominated by the prior; " else ""
    fit <- tryCatch(bayesmeta(y = d$yi, sigma = sqrt(d$vi), labels = d$study_id, mu.prior.mean = PRIOR_MU_MEAN, mu.prior.sd = PRIOR_MU_SD,
                              tau.prior = tau_prior(PRIOR_TAU_SCALE)), error = function(e) e)
    if (inherits(fit, "error")) { out[[i]] <- na_row(ab, me, k, paste0(k_note, "bayesmeta error: ", conditionMessage(fit))); next }
    row <- tryCatch({
      tibble(ability_id = ab, measure = me, k = k, mu_mean = fit$summary["mean", "mu"], mu_lb = fit$summary["95% lower", "mu"],
             mu_ub = fit$summary["95% upper", "mu"], tau_median = fit$summary["median", "tau"],
             p_mu_gt_0.2 = 1 - fit$pposterior(mu = SMD_THRESHOLD_SMALL), p_mu_gt_0.5 = 1 - fit$pposterior(mu = SMD_THRESHOLD_MODERATE),
             pred_lb = fit$summary["95% lower", "theta"], pred_ub = fit$summary["95% upper", "theta"],
             bf_10 = 1 / fit$bayesfactor[1, "mu=0"], mu_mean_wider = NA_real_, mu_mean_tighter = NA_real_,
             note = paste0(k_note, sprintf("mu~N(%s,%s), tau~halfN(%s) (placeholder pending Gate 5)", PRIOR_MU_MEAN, PRIOR_MU_SD, PRIOR_TAU_SCALE)))
    }, error = function(e) na_row(ab, me, k, paste0(k_note, "summary extraction error: ", conditionMessage(e))))
    for (nm in names(ALT_PRIORS)) {
      ap <- ALT_PRIORS[[nm]]
      f2 <- tryCatch(bayesmeta(y = d$yi, sigma = sqrt(d$vi), mu.prior.mean = ap$mu_mean, mu.prior.sd = ap$mu_sd, tau.prior = tau_prior(ap$tau_scale)), error = function(e) e)
      if (inherits(f2, "error")) row$note <- paste0(row$note, sprintf("; alt prior %s error: %s", nm, conditionMessage(f2)))
      else row[[paste0("mu_mean_", nm)]] <- f2$summary["mean", "mu"]
    }
    tryCatch({ png(file.path(OUT_DIR, sprintf("posterior_%s_%s.png", ab, me)), 1200, 900, res = 200); plot(fit, which = 2); dev.off() },
             error = function(e) { try(dev.off(), silent = TRUE); row$note <<- paste0(row$note, "; plot error: ", conditionMessage(e)) })
    out[[i]] <- row
  }
}
bayes <- if (length(out)) bind_rows(out) else na_row(character(), character(), integer(), character())[0, ]
bayes <- bayes %>% select(all_of(COLS_BAYES_POOLED))
write_csv(bayes, file.path(OUT_DIR, "bayes_pooled.csv"), na = "NA")
message(sprintf("Bayesian: %d ability x measure rows written (bayesmeta %s)", nrow(bayes), if (have_bayesmeta) "present" else "absent: note rows"))
