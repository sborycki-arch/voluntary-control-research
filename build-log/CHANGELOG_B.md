# CHANGELOG_B — analysis (fixer B, 2026-10-04)

Trace: s1-builder-B-20261004T115643Z-7a57. Environment: R 4.3.3, metafor 4.4.0, system library; bayesmeta and meta absent. Nothing committed.
All verification commands were run from the package root. SYN = analysis/synthetic; the two test masters are SYN/master_dryrun.csv and SYN/master_pooling.csv with VCR_POPULATION_SD=SYN/population_sd_synthetic.csv and VCR_GRADE_FINAL=SYN/grade_final_synthetic.csv.

## Register rows

R-009 | analysis/01_effect_sizes.R (new), analysis/00_load.R, analysis/constants.R, analysis/run_all.R | Raw-to-effect-size step implemented: SMD (escalc SMD, independent groups), SMCR (pre_post/crossover, pre_post_r or R_PREPOST_DEFAULT), PLO (n_responders/n_tested), OR (two binary rows), Z (delta/sigma_pop with the SCHEMA delta-method variance, only for `verified` population_sd rows matching ability + unit); SE->SD and CI95->SD conversions recorded in `derivation`; es_id = study_id_ability_NN; synthetic flag; exact contract item 2 columns; population SDs now used. run_all.R rebuilds from VCR_MASTER. | `bash analysis/synthetic/run_synthetic_tests.sh` -> 51 ok, 0 failures (output below): dry-run master gives PLO=1 SMCR=2 SMD=1 Z=1; pooling master gives 31 rows (PLO=3, SMCR=4, SMD=18, Z=6); header equals the contract string. closed
R-010 | analysis/02_frequentist.R (renamed from 01_frequentist.R, rewritten) | Every effect-size row gets its own interval in freq_individual.csv (yi ± 1.96·sqrt(vi); PLO and OR back-transformed in est_natural/ci_lb_natural/ci_ub_natural); k<3 units still appear in freq_pooled.csv with NA estimates and the note "k<3: not pooled; individual intervals in freq_individual.csv"; 04_sof.R expands them to one SoF row per study (source=individual). | Test suite: "dry-run: 5 individual rows (got 5)", "0 pooled estimates", "5 freq_pooled rows all k<3 noted", "SoF has 5 individual rows" all ok. closed
R-012 (pooling-unit part) | analysis/02_frequentist.R, analysis/03_bayesian.R, analysis/04_sof.R | Pooling unit is ability_id × measure using is_primary_outcome == yes rows only; non-primary rows are reported individually and never pooled; SoF joins grade_final on ability_id + outcome (= primary outcome_measure) so two outcomes no longer share an estimate; dependent-effect-size (multilevel) alternative stated as a Gate 5 decision in the 02 header comment. | Test suite: "non-primary row reported individually, not pooled" (A03 k sums to 10 = 5 SMD + 5 Z, the `no` row excluded) ok; "SoF joined GRADE on ability_id + outcome" ok; dry-run A03 outcome "axillary temperature" did not match the grade row "axillary temperature rise" and received the note "no grade_final row for this ability_id + outcome" (join is on both keys). partial — the aggregation rule for multiple timepoints/conditions per study is the statistician's Gate 5 item, not pre-empted
R-015 | analysis/setup.R | renv::snapshot(type = "all"); every installed analysis package loaded before capture.output(sessionInfo()); brms in tryCatch. | `Rscript -e 'parse("analysis/setup.R")'` -> parses OK. Not executed: CRAN unreachable here. partial (code only)
R-016 (guards only) | analysis/03_bayesian.R (renamed from 02_bayesian.R, rewritten), analysis/constants.R | requireNamespace guard; absent -> full contract column set with note "bayesmeta not installed" per ability × measure, one warning, normal return; present -> each bayesmeta call in tryCatch with the error in `note`, k = 1 allowed and noted "posterior dominated by the prior", alternative priors from constants.R. | Test suite: "bayes_pooled.csv header" and "bayes_pooled note rows when bayesmeta absent" ok on both masters; run_all.R exit 0 with the warning "bayesmeta not installed: bayes_pooled.csv carries note rows only". partial — the present-bayesmeta branch (summary indexing, k = 1 fit, BF) is not executable here
R-017 | analysis/00_load.R, analysis/run_all.R, analysis/constants.R, analysis/ENVIRONMENT.md | dir.create(OUT_DIR) is the first action after sourcing constants; working-directory check stops with a plain message in 00_load.R, run_all.R, setup.R and (via vcr_check_wd / the exists check) every script; run_all.R deletes analysis/outputs/* except .gitkeep before running; ENVIRONMENT.md states the root requirement. | Checkout copy without analysis/outputs/: `Rscript analysis/00_load.R` on the broken-provenance master -> "Error: 3 row(s) refused for missing provenance (rows 2,4,5); see analysis/outputs/REFUSED_missing_provenance.csv" and the CSV exists. `cd analysis && Rscript run_all.R` -> "Error: Run the analysis from the package root (the directory that contains analysis/00_load.R). Current working directory: .../vcr-build/analysis". Stale-output removal: the second run prints "Removed 18 stale output file(s)" (seen in SYN/run_pooling.log). closed
R-018 | analysis/00_load.R, analysis/constants.R | Validates design, lever_type, value_source, verification_route, stat_type, dispersion_type, is_primary_outcome against the SCHEMA vocabularies, ability_id against A01..A26 (semicolon-separated allowed), pre_post_r numeric in [-1, 1], condition_label non-blank (free text allowed), and skill_version and model non-blank (added to the provenance set); writes REFUSED_vocabulary.csv / REFUSED_missing_provenance.csv with a `reason` column and stops with a plain message. | Broken copies (messages pasted below): provenance copy -> 3 rows refused with reasons "location blank", "source_doi and source_url both blank", "model blank"; vocabulary copy -> 4 rows refused with reasons naming the field, the value and the allowed set. Also caught the generator's own blank dispersion_type on the prevalence row during the build (fixed to `none`). closed
R-067 | analysis/setup.R, analysis/ENVIRONMENT.md | `meta` removed from the install vector with a comment; ENVIRONMENT.md states that no script uses it and why metafor alone covers the REML/HKSJ model. | `grep -n "meta\b" analysis/*.R` -> only the comment in setup.R ("`meta` deliberately absent (R-067)"); no library(meta) anywhere. closed
R-069 | analysis/01_effect_sizes.R, analysis/constants.R, analysis/02_frequentist.R | Within-person route: SMCR via metafor::escalc(SMCR) from post (value) and pre (baseline_value/baseline_dispersion on the row, or the paired baseline/sham row), ri = pre_post_r when reported else R_PREPOST_DEFAULT = 0.5 labelled "placeholder pending the statistician co-author's decision at Gate 5" in `derivation`; mean_change rows handled; 02 re-pools every SMCR unit at R_PREPOST_SENS = 0.3 and 0.7 for the placeholder rows (freq_prepost_sensitivity.csv). | Test suite: dry-run pre_post row with blank r -> SMCR with the placeholder text ("placeholder r labelled in derivation" ok); crossover with pre_post_r 0.6 -> SMCR "r=0.6 (pre_post_r as reported)"; pooling A07 (two blank r) -> pooled est 1.133 [0.254, 2.012] at r=0.5, 1.153 at r=0.3, 1.113 at r=0.7 ("prepost sensitivity at r=0.3 and 0.7" ok). SMCR variance formula checked against escalc: 2(1-r)/n + yi²/(2n). closed
R-070 | analysis/03_bayesian.R, analysis/constants.R, analysis/01_effect_sizes.R | effect_sizes.csv carries `measure`; 03 routes only SMD/SMCR/Z (BAYES_SMD_MEASURES) into the SMD-scale priors and thresholds; PLO/OR units get the note "Beta-binomial / logit model: Gate 5" and no fit. | Routing code present and the absent-bayesmeta path exercised (A21 PLO row written with k=3 and a note, never fitted). partial — the present-bayesmeta branch cannot run here, so the PLO/OR note text is verified by reading only
R-072 | analysis/run_all.R, analysis/ENVIRONMENT.md | Outputs cleared first; MANIFEST.sha256 lists CSV files (sorted) then PNG files (sorted) and never itself or any input (inputs are not in analysis/outputs/); comparison rule for figures (data behind the figure, not bytes) stated in run_all.R and ENVIRONMENT.md. | Test suite: "MANIFEST does not list itself", "MANIFEST lists csv before png", "MANIFEST hashes verify (sha256sum -c)" ok. Two consecutive pooling runs: `diff manifest_run1 analysis/outputs/MANIFEST.sha256` -> identical (PNG bytes stable on this machine; cross-machine still untested, hence the data rule). closed
R-075 | analysis/02_frequentist.R, analysis/04_sof.R (renamed from 03_sof.R, rewritten) | freq_pooled.csv always has the full contract column set (NA where not pooled); 04_sof.R uses dplyr::any_of everywhere, handles an absent grade file (VCR_GRADE_FINAL) with empty GRADE columns and a note, and expands unpooled units to individual rows. | Dry-run configuration (five abilities, k = 1 each): `Rscript analysis/run_all.R` exit 0, "Summary of Findings: 8 rows (0 pooled, 5 individual)". Absent GRADE file: VCR_GRADE_FINAL=/nonexistent/grade_final.csv -> exit 0, note "GRADE columns empty: /nonexistent/grade_final.csv not found (set VCR_GRADE_FINAL)". closed
R-076 | analysis/run_all.R, analysis/setup.R, analysis/ENVIRONMENT.md | (a) run_all.R calls renv::load("analysis") when analysis/renv.lock exists, prints the library paths, and stops with a plain message if load fails or the pinned library lacks the core packages; VCR_IGNORE_RENV=1 bypasses deliberately and says so; otherwise prints "system library (no analysis/renv.lock); R 4.3.3, metafor 4.4.0". (b) setup.R installs brms in tryCatch, appends "brms not installed: <reason>" with the date to ENVIRONMENT.md on failure, and continues to snapshot and session_info. | (a) Temp copy with a minimal lockfile (not restored): "renv: loaded analysis/renv.lock; library paths: .../analysis/renv/library/..." then "Error: analysis/renv.lock loaded but the pinned library lacks metafor, dplyr, readr, digest: run renv::restore(...)" exit 1 — the pinned library is used, not the system one. Temp copy with a lockfile carrying Bioconductor refs: load fails offline -> plain message with the restore remedy, exit 1; with VCR_IGNORE_RENV=1 -> "system library (VCR_IGNORE_RENV set; analysis/renv.lock ignored)", exit 0. (b) parse-checked only (CRAN blocked). partial — (a) closed by execution, (b) by reading

## Final output of `bash analysis/synthetic/run_synthetic_tests.sh`

```
== configuration: dryrun
  ok   run_all.R exit 0 (got 0)
  ok   effect_sizes.csv exists
  ok   freq_pooled.csv exists
  ok   freq_individual.csv exists
  ok   bayes_pooled.csv exists
  ok   summary_of_findings.csv exists
  ok   MANIFEST.sha256 exists
  ok   effect_sizes.csv header
  ok   freq_pooled.csv header
  ok   freq_individual.csv header
  ok   bayes_pooled.csv header
  ok   MANIFEST does not list itself
  ok   MANIFEST lists csv before png
  ok   MANIFEST hashes verify (sha256sum -c)
  ok   bayes_pooled note rows when bayesmeta absent
  ok   dry-run: 5 individual rows (got 5)
  ok   dry-run: 0 pooled estimates (got 0)
  ok   dry-run: 5 freq_pooled rows all k<3 noted
  ok   dry-run: measures SMD, SMCR x2, PLO, Z present
  ok   dry-run: placeholder r labelled in derivation
  ok   dry-run: SoF has 5 individual rows with GRADE empty note
  log: analysis/synthetic/run_dryrun.log
    Loaded 7 rows, 5 abilities from analysis/synthetic/master_dryrun.csv; 1 verified population-SD rows (of 2) from analysis/synthetic/population_sd_synthetic.csv
    Effect sizes: 5 rows (PLO=1, SMCR=2, SMD=1, Z=1); 0 master row(s) produced none (effect_sizes_skipped.csv)
    Frequentist: 5 ability x measure units, 0 pooled (k>=3), 0 Egger test(s); 5 individual rows
    Bayesian: 5 ability x measure rows written (bayesmeta absent: note rows)
    Summary of Findings: 8 rows (0 pooled, 5 individual); GRADE from analysis/synthetic/grade_final_synthetic.csv
    Warning message:
    Rebuilt 12 outputs (12 csv, 0 png) from analysis/synthetic/master_dryrun.csv in 3.3 s; manifest analysis/outputs/MANIFEST.sha256
== configuration: pooling
  ok   run_all.R exit 0 (got 0)
  ok   effect_sizes.csv exists
  ok   freq_pooled.csv exists
  ok   freq_individual.csv exists
  ok   bayes_pooled.csv exists
  ok   summary_of_findings.csv exists
  ok   MANIFEST.sha256 exists
  ok   effect_sizes.csv header
  ok   freq_pooled.csv header
  ok   freq_individual.csv header
  ok   bayes_pooled.csv header
  ok   MANIFEST does not list itself
  ok   MANIFEST lists csv before png
  ok   MANIFEST hashes verify (sha256sum -c)
  ok   bayes_pooled note rows when bayesmeta absent
  ok   pooling: pooled estimate for A03
  ok   pooling: pooled estimate for A07
  ok   pooling: pooled estimate for A05
  ok   pooling: pooled estimate for A21
  ok   pooling: Egger row for A05
  ok   pooling: funnel PNG for A05
  ok   pooling: forest PNGs for the pooled units
  ok   pooling: Z pooled for A03 (verified population SD)
  ok   pooling: non-primary row reported individually, not pooled
  ok   pooling: SE-reported row converted (derivation)
  ok   pooling: prepost sensitivity at r=0.3 and 0.7
  ok   pooling: sensitivity rows (fixed_effect, exclude_n_i_le_3)
  ok   pooling: PLO natural-scale columns filled
  ok   pooling: SoF joined GRADE on ability_id + outcome
  ok   pooling: LOO rows written
  log: analysis/synthetic/run_pooling.log
    Loaded 43 rows, 4 abilities from analysis/synthetic/master_pooling.csv; 1 verified population-SD rows (of 2) from analysis/synthetic/population_sd_synthetic.csv
    Effect sizes: 31 rows (PLO=3, SMCR=4, SMD=18, Z=6); 0 master row(s) produced none (effect_sizes_skipped.csv)
    Frequentist: 5 ability x measure units, 5 pooled (k>=3), 1 Egger test(s); 31 individual rows
    Bayesian: 5 ability x measure rows written (bayesmeta absent: note rows)
    Summary of Findings: 5 rows (5 pooled, 0 individual); GRADE from analysis/synthetic/grade_final_synthetic.csv
    Warning message:
    Rebuilt 18 outputs (12 csv, 6 png) from analysis/synthetic/master_pooling.csv in 5.0 s; manifest analysis/outputs/MANIFEST.sha256
== synthetic tests: 0 failure(s)
```

## Refusal proofs (deliberately broken copies of SYN/master_dryrun.csv under the session scratchpad, vcr-refusal-test/)

Provenance (row 2 location blanked; row 4 source_doi and source_url blanked; row 5 model blanked):
```
$ VCR_MASTER=.../master_broken_provenance.csv Rscript analysis/run_all.R
== analysis/00_load.R
Error: 3 row(s) refused for missing provenance (rows 2,4,5); see analysis/outputs/REFUSED_missing_provenance.csv
Execution halted            (exit 1)
REFUSED_missing_provenance.csv reason column:
  synth_dry_rct_2001   | location blank
  synth_dry_cross_2003 | source_doi and source_url both blank
  synth_dry_cross_2003 | model blank
```
Controlled vocabulary (row 1 design=randomized; row 3 lever_type=hypnosis; row 6 verification_route=pdf; row 7 pre_post_r=1.4):
```
$ VCR_MASTER=.../master_broken_vocabulary.csv Rscript analysis/run_all.R
== analysis/00_load.R
Error: 4 row(s) refused for controlled-vocabulary violations (rows 1,3,6,7); see analysis/outputs/REFUSED_vocabulary.csv
Execution halted            (exit 1)
REFUSED_vocabulary.csv reason column:
  synth_dry_rct_2001     | design='randomized' not in {rct|crossover|nonrandomised_comparison|pre_post|case_report|case_series|prevalence_survey|other}
  synth_dry_prepost_2002 | lever_type='hypnosis' not in {feedback|breathing|muscle|imagery|suggestion|none|mixed|unclear}
  synth_dry_prev_2004    | verification_route='pdf' not in {pdf_full_text|html_full_text|supplement|abstract_only|not_opened}
  synth_dry_case_2005    | pre_post_r='1.4' not numeric in [-1, 1]
```
Provisional row (row 3 verification_route=abstract_only): "Error: 1 row(s) are provisional (abstract_only/not_opened; rows 3); resolve before analysis".

## Files
Modified: analysis/00_load.R, analysis/run_all.R, analysis/setup.R, analysis/ENVIRONMENT.md. Renamed (filesystem mv, uncommitted): 01_frequentist.R -> 02_frequentist.R, 02_bayesian.R -> 03_bayesian.R, 03_sof.R -> 04_sof.R (all three rewritten). New: analysis/constants.R, analysis/01_effect_sizes.R, analysis/synthetic/{make_synthetic_master.py, master_dryrun.csv, master_pooling.csv, population_sd_synthetic.csv, grade_final_synthetic.csv, run_synthetic_tests.sh, run_synthetic_tests.out, run_dryrun.log, run_pooling.log}, traces/prompts/fix_B_2026-10-04.md, CHANGELOG_B.md. analysis/outputs/ restored to .gitkeep only after testing. Extra outputs beyond the contract set (effect_sizes_inputs.csv, effect_sizes_skipped.csv, freq_loo.csv, freq_egger.csv, freq_sensitivity.csv, freq_prepost_sensitivity.csv, freq_subgroup.csv) are always written so downstream readers never meet a missing file.

## Not closed
- R-015: setup.R rewritten to spec but cannot execute here (CRAN 403); verified by parse only. Needs one run on a CRAN-reachable machine (route 1).
- R-016: guards closed; the bayesmeta-present branch (summary indexing, k = 1 behaviour, BF, posterior plot) is unverified until bayesmeta is installable. No prior predictive check added (BARG item belongs to the statistician's analysis plan).
- R-070: routing implemented and the measure column exists; the PLO/OR deferral note on the present-bayesmeta branch is verified by reading only.
- R-076 (b): setup.R brms tryCatch verified by reading only (same CRAN limitation).
- R-012: only the pooling-unit part was in scope; the dependent-effect-size aggregation rule (multiple timepoints/conditions per study) remains the statistician's Gate 5 decision and is flagged in the 02_frequentist.R header.
- R-038 (not mine): the environment route is Sean's; both the renv and the system-library routes are now exercised by run_all.R and documented.

## Open questions for Sean / the statistician co-author
1. Case reports and other rows with n = 1 and no dispersion: 01_effect_sizes.R gives them a Z effect size with Var(delta) = 2·sigma_pop²/n (each observation given the population variance), labelled a placeholder pending Gate 5. Is a Z row wanted for single-participant observations at all, or should they stay narrative only?
2. Z rows are written in addition to SMD/SMCR for the same pair whenever a verified population_sd row matches the ability and unit, giving two pooling units (e.g. A03 × SMD and A03 × Z) for one GRADE row. Confirm that the SoF should carry both, or name the primary scale per ability.
3. SMCR direction and standardiser: post − pre divided by the pre (baseline/comparator) SD, metafor's SMCR convention. Confirm, or specify SMCC (SD of change) where papers report it.
4. The grade_final `outcome` string must equal the primary row's outcome_measure exactly for the SoF join; a normalisation rule (case/whitespace) or an outcome id would be more robust. Who sets it at reconciliation?
5. Subgroup by lever_type ran on none of the synthetic units (single level each); the threshold (>= 2 levels with k >= 2) is in constants.R for the statistician to confirm.
