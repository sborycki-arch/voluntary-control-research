# Method 2: random-effects pooling with REML tau^2, Hartung-Knapp CIs, prediction intervals, LOO, Egger at k>=10.
suppressPackageStartupMessages({library(metafor); library(dplyr); library(readr)})
source("analysis/00_load.R")
# es_table: one row per study x ability with yi, vi on the chosen scale (built by the statistician agent from m;
# Hedges' g via escalc(measure="SMD") for continuous contrasts, "PLO" for prevalence, "OR" for binary).
es <- read_csv("analysis/outputs/effect_sizes.csv", show_col_types = FALSE)
results <- list(); loo <- list(); egger <- list()
for (ab in unique(es$ability_id)) {
  d <- filter(es, ability_id == ab)
  if (nrow(d) < 3) { results[[ab]] <- data.frame(ability_id = ab, k = nrow(d), note = "k<3: not pooled; individual intervals reported"); next }
  fit <- rma(yi, vi, data = d, method = "REML", test = "knha")
  pr <- predict(fit)
  results[[ab]] <- data.frame(ability_id = ab, k = fit$k, est = fit$beta[1], ci_lb = fit$ci.lb, ci_ub = fit$ci.ub,
                              pi_lb = pr$pi.lb, pi_ub = pr$pi.ub, tau2 = fit$tau2, I2 = fit$I2, p = fit$pval)
  loo[[ab]] <- cbind(ability_id = ab, as.data.frame(leave1out(fit)))
  if (fit$k >= 10) { rt <- regtest(fit); egger[[ab]] <- data.frame(ability_id = ab, z = rt$zval, p = rt$pval) }
  png(sprintf("analysis/outputs/forest_%s.png", ab), 1600, 200 + 60 * fit$k, res = 200); forest(fit, slab = d$study_id); dev.off()
  if (fit$k >= 10) { png(sprintf("analysis/outputs/funnel_%s.png", ab), 1200, 1200, res = 200); funnel(fit); dev.off() }
}
write_csv(bind_rows(results), "analysis/outputs/freq_pooled.csv")
if (length(loo)) write_csv(bind_rows(loo), "analysis/outputs/freq_loo.csv")
if (length(egger)) write_csv(bind_rows(egger), "analysis/outputs/freq_egger.csv")
# Sensitivity analyses (pre-specified): exclude n_condition <= 3; fixed-effect comparison; subgroup by lever_type.
