# 02_frequentist.R: Method 2, random-effects pooling per ability_id x measure on is_primary_outcome == yes rows
# (contract item 4; register R-010, R-011, R-012 pooling-unit part, R-075). REML tau^2, Knapp-Hartung CIs, prediction
# interval, leave-one-out, Egger regression test and funnel at k >= K_MIN_EGGER, forest PNG at k >= K_MIN_POOL.
# Below K_MIN_POOL nothing is pooled: freq_pooled.csv still carries the row (NA estimates, note filled) and every
# effect-size row is reported with its own interval in freq_individual.csv (charter D1).
# Dependent effect sizes: one primary row per study x ability enters pooling; non-primary rows and any additional
# timepoints are reported individually only. A multilevel / robust-variance alternative is a Gate 5 decision for the
# statistician co-author; nothing here aggregates dependent rows.
# Outputs: freq_pooled.csv (contract item 5 columns), freq_individual.csv (contract item 5 columns), freq_loo.csv,
# freq_egger.csv, freq_sensitivity.csv, freq_prepost_sensitivity.csv, freq_subgroup.csv, forest_<ability>_<measure>.png,
# funnel_<ability>_<measure>.png.
suppressPackageStartupMessages({library(metafor); library(dplyr); library(readr)})
if (!exists("vcr_loaded")) source("analysis/00_load.R")
source("analysis/constants.R")

es <- read_csv(file.path(OUT_DIR, "effect_sizes.csv"), show_col_types = FALSE,
               col_types = cols(.default = "c", yi = "d", vi = "d", n_i = "d", n_c = "d"))
inp_path <- file.path(OUT_DIR, "effect_sizes_inputs.csv")
inp <- if (file.exists(inp_path)) read_csv(inp_path, show_col_types = FALSE, col_types = cols(.default = "c")) else tibble(es_id = character())
prim <- es %>% filter(is_primary_outcome == "yes")
units <- prim %>% distinct(ability_id, measure) %>% arrange(ability_id, measure)

na_pooled <- function(ab, me, om, k, note) tibble(ability_id = ab, measure = me, outcome_measure = om, k = k, est = NA_real_,
  ci_lb = NA_real_, ci_ub = NA_real_, pi_lb = NA_real_, pi_ub = NA_real_, tau2 = NA_real_, I2 = NA_real_, p = NA_real_, note = note)
fit_row <- function(fit, ab, me, om, note) {
  pr <- predict(fit)
  tibble(ability_id = ab, measure = me, outcome_measure = om, k = fit$k, est = as.numeric(fit$beta[1]), ci_lb = fit$ci.lb, ci_ub = fit$ci.ub,
         pi_lb = pr$pi.lb, pi_ub = pr$pi.ub, tau2 = fit$tau2, I2 = fit$I2, p = fit$pval, note = note)
}
outcome_string <- function(d) paste(sort(unique(d$outcome_measure)), collapse = "; ")

pooled <- list(); loo <- list(); egger <- list(); sens <- list(); prepost <- list(); subgroup <- list()
for (u in seq_len(nrow(units))) {
  ab <- units$ability_id[u]; me <- units$measure[u]
  d <- prim %>% filter(ability_id == ab, measure == me) %>% arrange(study_id)
  om <- outcome_string(d)
  om_note <- if (length(unique(d$outcome_measure)) > 1) sprintf(" [%d distinct outcome_measure strings among primary rows]", length(unique(d$outcome_measure))) else ""
  tag <- sprintf("%s_%s", ab, me)
  if (nrow(d) < K_MIN_POOL) {
    pooled[[tag]] <- na_pooled(ab, me, om, nrow(d), sprintf("k<%d: not pooled; individual intervals in freq_individual.csv%s", K_MIN_POOL, om_note))
    sens[[tag]] <- tibble(ability_id = ab, measure = me, analysis = c("fixed_effect", "exclude_n_i_le_3", "subgroup_lever_type"), k = nrow(d),
                          est = NA_real_, ci_lb = NA_real_, ci_ub = NA_real_, note = sprintf("k<%d: not run", K_MIN_POOL))
    next
  }
  fit <- tryCatch(rma(yi, vi, data = d, method = "REML", test = "knha"), error = function(e) e)
  if (inherits(fit, "error")) { pooled[[tag]] <- na_pooled(ab, me, om, nrow(d), paste("rma failed:", conditionMessage(fit))); next }
  pooled[[tag]] <- fit_row(fit, ab, me, om, paste0("REML tau^2, Knapp-Hartung CI, prediction interval", om_note))
  loo[[tag]] <- bind_cols(tibble(ability_id = ab, measure = me, study_id = d$study_id, es_id = d$es_id), as.data.frame(leave1out(fit)))
  if (fit$k >= K_MIN_EGGER) {
    rt <- regtest(fit)   # Egger: model rma, predictor sei
    egger[[tag]] <- tibble(ability_id = ab, measure = me, k = fit$k, z = rt$zval, p = rt$pval, note = "regtest(model='rma', predictor='sei')")
    png(file.path(OUT_DIR, sprintf("funnel_%s.png", tag)), 1200, 1200, res = 200); funnel(fit, main = tag); dev.off()
  }
  png(file.path(OUT_DIR, sprintf("forest_%s.png", tag)), 1600, 300 + 60 * fit$k, res = 200)
  forest(fit, slab = d$study_id, header = c(tag, sprintf("%s [95%% CI]", me))); dev.off()
  # ---- sensitivity: fixed-effect comparison; exclusion of n_i <= N_SMALL_STUDY -----------------------------------
  fe <- rma(yi, vi, data = d, method = "FE")
  sens[[paste0(tag, "_fe")]] <- tibble(ability_id = ab, measure = me, analysis = "fixed_effect", k = fe$k, est = as.numeric(fe$beta[1]), ci_lb = fe$ci.lb, ci_ub = fe$ci.ub,
                                       note = "method='FE' comparison with the REML/knha estimate in freq_pooled.csv")
  d_big <- d %>% filter(is.na(n_i) | n_i > N_SMALL_STUDY)
  sens[[paste0(tag, "_small")]] <- if (nrow(d_big) == nrow(d)) {
    tibble(ability_id = ab, measure = me, analysis = "exclude_n_i_le_3", k = nrow(d), est = as.numeric(fit$beta[1]), ci_lb = fit$ci.lb, ci_ub = fit$ci.ub, note = "no row with n_i <= 3; identical to main analysis")
  } else if (nrow(d_big) >= K_MIN_POOL) {
    f2 <- rma(yi, vi, data = d_big, method = "REML", test = "knha")
    tibble(ability_id = ab, measure = me, analysis = "exclude_n_i_le_3", k = f2$k, est = as.numeric(f2$beta[1]), ci_lb = f2$ci.lb, ci_ub = f2$ci.ub, note = sprintf("%d row(s) with n_i <= 3 excluded", nrow(d) - nrow(d_big)))
  } else tibble(ability_id = ab, measure = me, analysis = "exclude_n_i_le_3", k = nrow(d_big), est = NA_real_, ci_lb = NA_real_, ci_ub = NA_real_, note = sprintf("k<%d after excluding n_i <= 3: not run", K_MIN_POOL))
  # ---- subgroup by lever_type when >= 2 levels each with k >= K_MIN_SUBGROUP_LEVEL -----------------------------------
  lv <- table(d$lever_type); lv_ok <- names(lv)[lv >= K_MIN_SUBGROUP_LEVEL]
  if (length(lv_ok) >= 2) {
    d_sub <- d %>% filter(lever_type %in% lv_ok)
    fs <- rma(yi, vi, mods = ~ lever_type, data = d_sub, method = "REML", test = "knha")
    for (l in lv_ok) {
      fl <- rma(yi, vi, data = filter(d_sub, lever_type == l), method = "REML", test = "knha")
      subgroup[[paste(tag, l)]] <- tibble(ability_id = ab, measure = me, lever_type = l, k = fl$k, est = as.numeric(fl$beta[1]), ci_lb = fl$ci.lb, ci_ub = fl$ci.ub, QM_p = fs$QMp,
                                          note = "per-level REML/knha fit; QM_p from the moderator model")
    }
    sens[[paste0(tag, "_sub")]] <- tibble(ability_id = ab, measure = me, analysis = "subgroup_lever_type", k = nrow(d_sub), est = NA_real_, ci_lb = NA_real_, ci_ub = NA_real_,
                                          note = sprintf("run: levels %s; QM p=%s; see freq_subgroup.csv", paste(lv_ok, collapse = "/"), signif(fs$QMp, 3)))
  } else sens[[paste0(tag, "_sub")]] <- tibble(ability_id = ab, measure = me, analysis = "subgroup_lever_type", k = nrow(d), est = NA_real_, ci_lb = NA_real_, ci_ub = NA_real_,
                                               note = sprintf("not run: fewer than 2 lever_type levels with k>=%d (levels: %s)", K_MIN_SUBGROUP_LEVEL, paste(sprintf("%s=%d", names(lv), as.integer(lv)), collapse = ", ")))
  # ---- SMCR: re-pool at each R_PREPOST_SENS value for rows that used the placeholder --------------------------------
  if (me == "SMCR" && nrow(inp)) {
    di <- d %>% left_join(inp %>% select(any_of(c("es_id", "r_used", "r_source"))), by = "es_id")
    n_placeholder <- sum(di$r_source == "placeholder", na.rm = TRUE)
    for (rr in R_PREPOST_SENS) {
      # yi does not depend on r; vi = 2(1 - r)/n + yi^2/(2n) (metafor SMCR). Reported r values are kept.
      ds <- di %>% mutate(vi = ifelse(r_source == "placeholder", 2 * (1 - rr) / n_i + yi^2 / (2 * n_i), vi))
      fr <- rma(yi, vi, data = ds, method = "REML", test = "knha")
      prepost[[paste(tag, rr)]] <- fit_row(fr, ab, me, om, sprintf("r=%s for %d placeholder row(s) (reported pre_post_r kept for %d); R_PREPOST_DEFAULT=%s is a placeholder pending the statistician co-author's decision at Gate 5",
                                                                   rr, n_placeholder, nrow(di) - n_placeholder, R_PREPOST_DEFAULT)) %>% mutate(r_prepost = rr, .before = note)
    }
  }
}

pooled_df <- if (length(pooled)) bind_rows(pooled) else na_pooled(character(), character(), character(), integer(), character())[0, ]
pooled_df <- pooled_df %>% select(all_of(COLS_FREQ_POOLED))
write_csv(pooled_df, file.path(OUT_DIR, "freq_pooled.csv"), na = "NA")

# ---- individual intervals for every effect-size row (charter D1; register R-010) --------------------------------------
k_tab <- prim %>% count(ability_id, measure, name = "k_ability")
indiv <- es %>% left_join(k_tab, by = c("ability_id", "measure")) %>%
  mutate(k_ability = ifelse(is.na(k_ability), 0L, k_ability), ci_lb = yi - 1.96 * sqrt(vi), ci_ub = yi + 1.96 * sqrt(vi),
         est_natural = case_when(measure == "PLO" ~ plogis(yi), measure == "OR" ~ exp(yi), TRUE ~ NA_real_),
         ci_lb_natural = case_when(measure == "PLO" ~ plogis(ci_lb), measure == "OR" ~ exp(ci_lb), TRUE ~ NA_real_),
         ci_ub_natural = case_when(measure == "PLO" ~ plogis(ci_ub), measure == "OR" ~ exp(ci_ub), TRUE ~ NA_real_)) %>%
  select(all_of(COLS_FREQ_INDIVIDUAL))
write_csv(indiv, file.path(OUT_DIR, "freq_individual.csv"), na = "NA")

empty_or <- function(lst, template) if (length(lst)) bind_rows(lst) else template
write_csv(empty_or(loo, tibble(ability_id = character(), measure = character(), study_id = character(), es_id = character())), file.path(OUT_DIR, "freq_loo.csv"), na = "NA")
write_csv(empty_or(egger, tibble(ability_id = character(), measure = character(), k = integer(), z = numeric(), p = numeric(), note = character())), file.path(OUT_DIR, "freq_egger.csv"), na = "NA")
write_csv(empty_or(sens, tibble(ability_id = character(), measure = character(), analysis = character(), k = integer(), est = numeric(), ci_lb = numeric(), ci_ub = numeric(), note = character())), file.path(OUT_DIR, "freq_sensitivity.csv"), na = "NA")
write_csv(empty_or(prepost, na_pooled(character(), character(), character(), integer(), character())[0, ] %>% mutate(r_prepost = numeric(), .before = note)), file.path(OUT_DIR, "freq_prepost_sensitivity.csv"), na = "NA")
write_csv(empty_or(subgroup, tibble(ability_id = character(), measure = character(), lever_type = character(), k = integer(), est = numeric(), ci_lb = numeric(), ci_ub = numeric(), QM_p = numeric(), note = character())), file.path(OUT_DIR, "freq_subgroup.csv"), na = "NA")
message(sprintf("Frequentist: %d ability x measure units, %d pooled (k>=%d), %d Egger test(s); %d individual rows",
                nrow(pooled_df), sum(!is.na(pooled_df$est)), K_MIN_POOL, length(egger), nrow(indiv)))
