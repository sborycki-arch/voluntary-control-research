# Method 3: Bayesian normal-normal hierarchical model with the declared priors (Gate 0 defaults until the
# statistician co-author sets them; locked at Gate 5). Reported to BARG.
suppressPackageStartupMessages({library(bayesmeta); library(dplyr); library(readr)})
es <- read_csv("analysis/outputs/effect_sizes.csv", show_col_types = FALSE)
mu_prior <- c(0, 1)                                   # Normal(0, 1) on the SMD scale
tau_prior <- function(t) dhalfnormal(t, scale = 0.5)  # half-Normal(0, 0.5)
alt_priors <- list(wider = list(mu = c(0, 2), tau = function(t) dhalfnormal(t, scale = 1)),
                   tighter = list(mu = c(0, 0.5), tau = function(t) dhalfnormal(t, scale = 0.25)))
out <- list()
for (ab in unique(es$ability_id)) {
  d <- filter(es, ability_id == ab)
  fit <- bayesmeta(y = d$yi, sigma = sqrt(d$vi), labels = d$study_id, mu.prior.mean = mu_prior[1], mu.prior.sd = mu_prior[2], tau.prior = tau_prior)
  row <- data.frame(ability_id = ab, k = nrow(d), mu_mean = fit$summary["mean", "mu"], mu_lb = fit$summary["95% lower", "mu"],
                    mu_ub = fit$summary["95% upper", "mu"], tau_median = fit$summary["median", "tau"],
                    p_mu_gt_0.2 = 1 - fit$pposterior(mu = 0.2), p_mu_gt_0.5 = 1 - fit$pposterior(mu = 0.5),
                    pred_lb = fit$summary["95% lower", "theta"], pred_ub = fit$summary["95% upper", "theta"],
                    bf_10 = 1 / fit$bayesfactor[1, "mu=0"])
  for (nm in names(alt_priors)) {
    f2 <- bayesmeta(y = d$yi, sigma = sqrt(d$vi), mu.prior.mean = alt_priors[[nm]]$mu[1], mu.prior.sd = alt_priors[[nm]]$mu[2], tau.prior = alt_priors[[nm]]$tau)
    row[[paste0("mu_mean_", nm)]] <- f2$summary["mean", "mu"]
  }
  out[[ab]] <- row
  png(sprintf("analysis/outputs/posterior_%s.png", ab), 1200, 900, res = 200); plot(fit, which = 2); dev.off()
}
write_csv(bind_rows(out), "analysis/outputs/bayes_pooled.csv")
# Prevalence abilities: Beta-binomial hierarchical model (brms) or logit-scale bayesmeta; add at Gate 5.
