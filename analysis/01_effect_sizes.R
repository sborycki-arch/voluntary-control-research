# 01_effect_sizes.R: compute effect sizes from the master file (SCHEMA.md convention: computed in analysis code, never
# by extractors; register R-009, R-069). Writes analysis/outputs/effect_sizes.csv with exactly the contract item 2
# columns, plus effect_sizes_inputs.csv (ingredients, used by the pre/post-r sensitivity in 02) and
# effect_sizes_skipped.csv (rows that produced no effect size, with the reason).
#
# Measures: SMD  independent groups (rct, nonrandomised_comparison), metafor::escalc(measure = "SMD") = Hedges' g
#           SMCR within-person (pre_post, crossover; case_series/other with baseline on the row), escalc("SMCR") with
#                ri = pre_post_r or R_PREPOST_DEFAULT (placeholder pending the statistician co-author's decision at Gate 5)
#           PLO  logit proportion from n_responders / n_tested (prevalence designs)
#           OR   log odds ratio when the intervention and comparator rows both carry n_responders / n_tested
#           Z    delta / sigma_pop with delta-method variance (SCHEMA.md) when a `verified` population_sd row matches
#                the ability_id and unit; written in addition to SMD/SMCR for the same pair
# Pairing: an intervention row is paired with the row of the same study_id + outcome_measure + timepoint whose
# condition_label equals the intervention row's comparator_label. Within-person rows may instead carry the pre value in
# baseline_value / baseline_dispersion on the same row (SCHEMA.md).
# SE -> SD: sd = se * sqrt(n). CI95 -> SD: sd = (hi - lo) / (2 * 1.96) * sqrt(n). Recorded in `derivation`.
suppressPackageStartupMessages({library(metafor); library(dplyr); library(readr)})
if (!exists("vcr_loaded")) source("analysis/00_load.R")
source("analysis/constants.R")

# ---- helpers ---------------------------------------------------------------------------------------------------------
fmt <- function(x, d = 5) ifelse(is.na(x), "NA", as.character(signif(x, d)))
# SD from the row's dispersion fields; returns list(sd, text)
sd_from <- function(type, disp, lo, hi, n, label = "SD") {
  type <- ifelse(is.na(type), "", type)
  if (type == "SD" && !is.na(disp)) return(list(sd = disp, text = sprintf("%s=%s (SD as printed)", label, fmt(disp))))
  if (type == "SE" && !is.na(disp) && !is.na(n)) return(list(sd = disp * sqrt(n), text = sprintf("%s=se*sqrt(n)=%s*sqrt(%d)=%s", label, fmt(disp), as.integer(n), fmt(disp * sqrt(n)))))
  if (type == "CI95" && !is.na(lo) && !is.na(hi) && !is.na(n)) {
    sd <- (hi - lo) / (2 * 1.96) * sqrt(n)
    return(list(sd = sd, text = sprintf("%s=(hi-lo)/(2*1.96)*sqrt(n)=(%s-%s)/3.92*sqrt(%d)=%s", label, fmt(hi), fmt(lo), as.integer(n), fmt(sd))))
  }
  list(sd = NA_real_, text = sprintf("%s not derivable (dispersion_type='%s')", label, type))
}
# Verified population-SD row matching ability and unit (first match); NULL if none
pop_match <- function(ab, unit) {
  if (nrow(pop) == 0 || is.na(unit) || unit == "") return(NULL)
  hit <- pop %>% filter(vapply(strsplit(ability_id, ";"), function(a) ab %in% trimws(a), logical(1)),
                        tolower(unit) == tolower(!!unit), !is.na(sd), sd > 0)
  if (nrow(hit) == 0) NULL else hit[1, ]
}
# Z = delta / sigma_pop with delta-method variance (SCHEMA.md). var_delta may be NA (then the placeholder applies).
z_row <- function(delta, var_delta, pm, n_i, n_c, within = FALSE) {
  sigma <- pm$sd; n_pop <- pm$n
  txt <- sprintf("Z=delta/sigma_pop=%s/%s", fmt(delta), fmt(sigma))
  if (is.na(var_delta)) {
    # No SD on the row (e.g. case report, n = 1): each observation is given the population variance.
    var_delta <- if (within) 2 * sigma^2 / n_i else sigma^2 * (1 / n_i + 1 / n_c)
    txt <- paste0(txt, sprintf("; Var(delta) not estimable from the row (no SD): %s=%s used (placeholder pending the statistician co-author's decision at Gate 5)",
                               if (within) "2*sigma_pop^2/n" else "sigma_pop^2*(1/n_i+1/n_c)", fmt(var_delta)))
  } else txt <- paste0(txt, sprintf("; Var(delta)=%s", fmt(var_delta)))
  var_sigma <- if (!is.na(n_pop) && n_pop > 1) sigma^2 / (2 * (n_pop - 1)) else 0
  txt <- paste0(txt, if (!is.na(n_pop) && n_pop > 1) sprintf("; Var(sigma)=sigma^2/(2(n_pop-1)), n_pop=%d", as.integer(n_pop)) else "; Var(sigma)=0 (population_sd n blank)")
  vi <- var_delta / sigma^2 + delta^2 * var_sigma / sigma^4
  txt <- paste0(txt, sprintf("; Var(z)=Var(delta)/sigma^2+delta^2*Var(sigma)/sigma^4=%s; population_sd source: %s", fmt(vi), pm$source_citation))
  list(yi = delta / sigma, vi = vi, text = txt, sigma = sigma, n_pop = n_pop)
}

out <- list(); inputs <- list(); skipped <- list()
emit <- function(r, ab, measure, yi, vi, n_i, n_c, text, inp = list()) {
  out[[length(out) + 1]] <<- tibble(study_id = r$study_id, ability_id = ab, outcome_measure = r$outcome_measure,
    timepoint = r$timepoint, design = r$design, lever_type = r$lever_type, measure = measure, yi = as.numeric(yi),
    vi = as.numeric(vi), n_i = n_i, n_c = n_c, is_primary_outcome = r$is_primary_outcome,
    synthetic = ifelse(startsWith(r$study_id, "synth_"), "yes", "no"), derivation = text)
  inputs[[length(inputs) + 1]] <<- as_tibble(c(list(study_id = r$study_id, ability_id = ab, outcome_measure = r$outcome_measure,
    timepoint = r$timepoint, measure = measure), inp))
}
skip <- function(r, reason) skipped[[length(skipped) + 1]] <<- tibble(study_id = r$study_id, ability_id = r$ability_id,
  outcome_measure = r$outcome_measure, timepoint = r$timepoint, condition_label = r$condition_label, design = r$design, reason = reason)

has_binary <- function(r) !is.na(r$n_responders) && !is.na(r$n_tested) && r$n_tested > 0
# Pre-pass: mark rows that serve as the comparator of another row, so they are consumed rather than reported as skipped.
m$.consumed <- FALSE
for (i in seq_len(nrow(m))) {
  cl <- m$comparator_label[i]
  if (!is.na(cl) && cl != "") {
    idx <- which(m$study_id == m$study_id[i] & m$outcome_measure == m$outcome_measure[i] & m$timepoint == m$timepoint[i] &
                 m$condition_label == cl & seq_len(nrow(m)) != i)
    m$.consumed[idx] <- TRUE
  }
}

for (i in seq_len(nrow(m))) {
  r <- m[i, ]
  if (m$.consumed[i] && (is.na(r$comparator_label) || r$comparator_label == "")) next   # comparator row
  abilities <- trimws(strsplit(r$ability_id, ";")[[1]])
  multi_note <- if (length(abilities) > 1) sprintf(" [master row informs %d abilities: %s]", length(abilities), r$ability_id) else ""
  # ---- locate the comparator row, if any --------------------------------------------------------------------------
  cmp <- NULL
  if (!is.na(r$comparator_label) && r$comparator_label != "") {
    idx <- which(m$study_id == r$study_id & m$outcome_measure == r$outcome_measure & m$timepoint == r$timepoint &
                 m$condition_label == r$comparator_label & seq_len(nrow(m)) != i)
    if (length(idx) == 0) { skip(r, sprintf("comparator_label '%s' matches no row of the same study_id/outcome_measure/timepoint", r$comparator_label)); next }
    if (length(idx) > 1) { skip(r, sprintf("comparator_label '%s' matches %d rows (ambiguous)", r$comparator_label, length(idx))); next }
    cmp <- m[idx, ]
  }
  sd_i <- sd_from(r$dispersion_type, r$dispersion_value, r$ci_low, r$ci_high, r$n_condition, "SD_i")
  produced <- 0L
  for (ab in abilities) {
    pm <- pop_match(ab, r$unit)
    # ---- independent groups: OR, SMD, Z -------------------------------------------------------------------------
    if (r$design %in% DESIGNS_INDEPENDENT) {
      if (is.null(cmp)) { skip(r, "independent-group design without comparator_label"); break }
      if (has_binary(r) && has_binary(cmp)) {
        e <- escalc(measure = "OR", ai = r$n_responders, bi = r$n_tested - r$n_responders, ci = cmp$n_responders, di = cmp$n_tested - cmp$n_responders)
        emit(r, ab, "OR", e$yi, e$vi, r$n_tested, cmp$n_tested,
             sprintf("log OR via metafor::escalc(OR): a=%d b=%d c=%d d=%d (intervention responders/non-responders vs '%s')%s",
                     as.integer(r$n_responders), as.integer(r$n_tested - r$n_responders), as.integer(cmp$n_responders), as.integer(cmp$n_tested - cmp$n_responders), cmp$condition_label, multi_note))
        produced <- produced + 1L
      }
      sd_c <- sd_from(cmp$dispersion_type, cmp$dispersion_value, cmp$ci_low, cmp$ci_high, cmp$n_condition, "SD_c")
      if (!is.na(r$value) && !is.na(cmp$value) && !is.na(sd_i$sd) && !is.na(sd_c$sd) && !is.na(r$n_condition) && !is.na(cmp$n_condition) &&
          r$n_condition >= 2 && cmp$n_condition >= 2) {
        e <- escalc(measure = "SMD", m1i = r$value, m2i = cmp$value, sd1i = sd_i$sd, sd2i = sd_c$sd, n1i = r$n_condition, n2i = cmp$n_condition)
        emit(r, ab, "SMD", e$yi, e$vi, r$n_condition, cmp$n_condition,
             sprintf("Hedges' g via metafor::escalc(SMD): m_i=%s m_c=%s n_i=%d n_c=%d (vs '%s'); %s; %s%s", fmt(r$value), fmt(cmp$value),
                     as.integer(r$n_condition), as.integer(cmp$n_condition), cmp$condition_label, sd_i$text, sd_c$text, multi_note),
             list(m1 = r$value, m2 = cmp$value, sd1 = sd_i$sd, sd2 = sd_c$sd, n1 = r$n_condition, n2 = cmp$n_condition, r_used = NA_real_, r_source = "na"))
        produced <- produced + 1L
        if (!is.null(pm)) {
          z <- z_row(r$value - cmp$value, sd_i$sd^2 / r$n_condition + sd_c$sd^2 / cmp$n_condition, pm, r$n_condition, cmp$n_condition)
          emit(r, ab, "Z", z$yi, z$vi, r$n_condition, cmp$n_condition, paste0("delta=m_i-m_c; Var(delta)=SD_i^2/n_i+SD_c^2/n_c; ", z$text, multi_note),
               list(m1 = r$value, m2 = cmp$value, sd1 = sd_i$sd, sd2 = sd_c$sd, n1 = r$n_condition, n2 = cmp$n_condition, r_used = NA_real_, r_source = "na", sigma_pop = z$sigma, n_pop = z$n_pop))
          produced <- produced + 1L
        }
      } else if (!(has_binary(r) && has_binary(cmp))) {
        skip(r, sprintf("SMD not computable: value/SD/n missing on intervention or comparator row (%s; %s)", sd_i$text, sd_c$text)); break
      }
      next
    }
    # ---- prevalence: PLO --------------------------------------------------------------------------------------------
    if (r$design == "prevalence_survey" || (is.null(cmp) && has_binary(r) && is.na(r$value) && is.na(r$baseline_value))) {
      if (!has_binary(r)) { skip(r, "prevalence design without n_responders/n_tested"); break }
      e <- escalc(measure = "PLO", xi = r$n_responders, ni = r$n_tested)
      emit(r, ab, "PLO", e$yi, e$vi, r$n_tested, NA_real_,
           sprintf("logit proportion via metafor::escalc(PLO): x=%d n=%d (p=%s)%s", as.integer(r$n_responders), as.integer(r$n_tested), fmt(r$n_responders / r$n_tested), multi_note),
           list(x = r$n_responders, n1 = r$n_tested, r_used = NA_real_, r_source = "na"))
      produced <- produced + 1L
      next
    }
    # ---- within-person (pre_post, crossover) and single-arm designs with a baseline: SMCR, Z -------------------------
    # Pre value: baseline_value on the row (SCHEMA.md), else the paired comparator row (baseline/sham/control).
    if (!is.na(r$baseline_value) || !is.null(cmp)) {
      if (!is.na(r$baseline_value)) {
        sd_pre <- sd_from(r$dispersion_type, r$baseline_dispersion, NA, NA, r$n_condition, "SD_pre")
        if (r$stat_type == "mean_change") { m_post <- r$value; m_pre <- 0; delta <- r$value; pre_txt <- sprintf("value is mean change=%s; baseline_dispersion read as pre SD", fmt(r$value)) }
        else { m_post <- r$value; m_pre <- r$baseline_value; delta <- r$value - r$baseline_value; pre_txt <- sprintf("post=%s pre=%s (baseline_value on the same row)", fmt(r$value), fmt(r$baseline_value)) }
        sd_post <- sd_i; n <- r$n_condition; n_c <- r$n_condition
      } else {
        sd_pre <- sd_from(cmp$dispersion_type, cmp$dispersion_value, cmp$ci_low, cmp$ci_high, cmp$n_condition, "SD_pre")
        m_post <- r$value; m_pre <- cmp$value; delta <- r$value - cmp$value; sd_post <- sd_i; n <- r$n_condition; n_c <- cmp$n_condition
        pre_txt <- sprintf("post=%s pre/comparator=%s (row '%s', same participants)", fmt(r$value), fmt(cmp$value), cmp$condition_label)
      }
      design_note <- if (r$design %in% DESIGNS_WITHIN) "" else sprintf(" [design=%s treated as within-person]", r$design)
      r_used <- if (!is.na(r$pre_post_r)) r$pre_post_r else R_PREPOST_DEFAULT
      r_text <- if (!is.na(r$pre_post_r)) sprintf("r=%s (pre_post_r as reported)", fmt(r$pre_post_r)) else
        sprintf("r=%s (R_PREPOST_DEFAULT: placeholder pending the statistician co-author's decision at Gate 5; pre_post_r blank)", fmt(R_PREPOST_DEFAULT))
      if (!is.na(delta) && !is.na(sd_pre$sd) && sd_pre$sd > 0 && !is.na(n) && n >= 2) {
        e <- escalc(measure = "SMCR", m1i = m_post, m2i = m_pre, sd1i = sd_pre$sd, ni = n, ri = r_used)
        emit(r, ab, "SMCR", e$yi, e$vi, n, n_c,
             sprintf("SMCR via metafor::escalc(SMCR) (post-pre)/SD_pre with small-sample correction: %s; %s; n=%d; %s; vi=2(1-r)/n+yi^2/(2n)%s%s",
                     pre_txt, sd_pre$text, as.integer(n), r_text, design_note, multi_note),
             list(m1 = m_post, m2 = m_pre, sd1 = sd_pre$sd, sd2 = sd_post$sd, n1 = n, n2 = n_c, r_used = r_used,
                  r_source = ifelse(is.na(r$pre_post_r), "placeholder", "reported")))
        produced <- produced + 1L
      }
          if (!is.null(pm) && !is.na(delta)) {
        var_delta <- if (!is.na(sd_pre$sd) && !is.na(n) && n >= 2) {
          sp <- ifelse(is.na(sd_post$sd), sd_pre$sd, sd_post$sd)
          (sd_pre$sd^2 + sp^2 - 2 * r_used * sd_pre$sd * sp) / n
        } else NA_real_
        z <- z_row(delta, var_delta, pm, ifelse(is.na(n), 1, n), n_c, within = TRUE)
        emit(r, ab, "Z", z$yi, z$vi, ifelse(is.na(n), 1, n), n_c,
             paste0("delta=post-pre (", pre_txt, "); ", if (!is.na(var_delta)) sprintf("Var(delta)=(SD_pre^2+SD_post^2-2*r*SD_pre*SD_post)/n with %s; ", r_text) else "", z$text, design_note, multi_note),
             list(m1 = m_post, m2 = m_pre, sd1 = sd_pre$sd, sd2 = sd_post$sd, n1 = ifelse(is.na(n), 1, n), n2 = n_c, r_used = r_used,
                  r_source = ifelse(is.na(r$pre_post_r), "placeholder", "reported"), sigma_pop = z$sigma, n_pop = z$n_pop))
        produced <- produced + 1L
      }
      if (produced == 0L) { skip(r, sprintf("within-person effect size not computable: %s; n=%s; %s", sd_pre$text, fmt(n, 1), if (is.null(pm)) "no verified population_sd row for this ability/unit" else "pop SD present but delta missing")); break }
      next
    }
      skip(r, "no comparator_label, no baseline_value and no n_responders/n_tested")
    break
  }
}

es <- if (length(out)) bind_rows(out) else tibble(study_id = character(), ability_id = character(), outcome_measure = character(),
  timepoint = character(), design = character(), lever_type = character(), measure = character(), yi = numeric(), vi = numeric(),
  n_i = numeric(), n_c = numeric(), is_primary_outcome = character(), synthetic = character(), derivation = character())
es <- es %>% group_by(study_id, ability_id) %>% mutate(es_id = sprintf("%s_%s_%02d", study_id, ability_id, row_number())) %>% ungroup() %>%
  select(all_of(COLS_EFFECT_SIZES))
write_csv(es, file.path(OUT_DIR, "effect_sizes.csv"), na = "NA")
inp <- if (length(inputs)) bind_rows(inputs) else tibble(es_id = character())  # header-only file when nothing was computed
if (nrow(inp)) { inp$es_id <- es$es_id; inp <- inp %>% select(es_id, everything()) }
write_csv(inp, file.path(OUT_DIR, "effect_sizes_inputs.csv"), na = "NA")
sk <- if (length(skipped)) bind_rows(skipped) else
  tibble(study_id = character(), ability_id = character(), outcome_measure = character(), timepoint = character(), condition_label = character(), design = character(), reason = character())
write_csv(sk, file.path(OUT_DIR, "effect_sizes_skipped.csv"), na = "NA")
message(sprintf("Effect sizes: %d rows (%s); %d master row(s) produced none (effect_sizes_skipped.csv)", nrow(es),
                paste(sprintf("%s=%d", names(table(es$measure)), as.integer(table(es$measure))), collapse = ", "), nrow(sk)))
