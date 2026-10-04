#!/usr/bin/env bash
# Runs analysis/run_all.R on the two SYNTHETIC masters and asserts the contract (BUILD_CONTRACT.md items 2, 5, 10).
# Run from the package root: bash analysis/synthetic/run_synthetic_tests.sh
set -u
cd "$(dirname "$0")/../.." || exit 2
[ -f analysis/00_load.R ] || { echo "FAIL: not at the package root"; exit 2; }
SYN=analysis/synthetic; OUT=analysis/outputs; fails=0
H_POOLED='ability_id,measure,outcome_measure,k,est,ci_lb,ci_ub,pi_lb,pi_ub,tau2,I2,p,note'
H_INDIV='es_id,study_id,ability_id,measure,outcome_measure,yi,ci_lb,ci_ub,k_ability,est_natural,ci_lb_natural,ci_ub_natural'
H_BAYES='ability_id,measure,k,mu_mean,mu_lb,mu_ub,tau_median,p_mu_gt_0.2,p_mu_gt_0.5,pred_lb,pred_ub,bf_10,mu_mean_wider,mu_mean_tighter,note'
H_ES='es_id,study_id,ability_id,outcome_measure,timepoint,design,lever_type,measure,yi,vi,n_i,n_c,is_primary_outcome,synthetic,derivation'
ok()   { echo "  ok   $1"; }
fail() { echo "  FAIL $1"; fails=$((fails+1)); }
check() { if eval "$2"; then ok "$1"; else fail "$1"; fi; }
header_is() { [ "$(head -1 "$1" | tr -d '\r')" = "$2" ]; }

python3 "$SYN/make_synthetic_master.py" >/dev/null || { echo "FAIL: generator"; exit 2; }
for cfg in dryrun pooling; do
  echo "== configuration: $cfg"
  VCR_MASTER="$SYN/master_$cfg.csv" VCR_POPULATION_SD="$SYN/population_sd_synthetic.csv" VCR_GRADE_FINAL="$SYN/grade_final_synthetic.csv" \
    Rscript analysis/run_all.R > "$SYN/run_$cfg.log" 2>&1; rc=$?
  check "run_all.R exit 0 (got $rc)" "[ $rc -eq 0 ]"
  for f in effect_sizes.csv freq_pooled.csv freq_individual.csv bayes_pooled.csv summary_of_findings.csv MANIFEST.sha256; do
    check "$f exists" "[ -s $OUT/$f ]"
  done
  check "effect_sizes.csv header"  "header_is $OUT/effect_sizes.csv \"\$H_ES\""
  check "freq_pooled.csv header"   "header_is $OUT/freq_pooled.csv \"\$H_POOLED\""
  check "freq_individual.csv header" "header_is $OUT/freq_individual.csv \"\$H_INDIV\""
  check "bayes_pooled.csv header"  "header_is $OUT/bayes_pooled.csv \"\$H_BAYES\""
  check "MANIFEST does not list itself" "! grep -q MANIFEST $OUT/MANIFEST.sha256"
  check "MANIFEST lists csv before png" "python3 -c \"
import sys; names=[l.split()[-1] for l in open('$OUT/MANIFEST.sha256')]
csv=[n for n in names if n.endswith('.csv')]; png=[n for n in names if n.endswith('.png')]
sys.exit(0 if names==csv+png and csv else 1)\""
  check "MANIFEST hashes verify (sha256sum -c)" "(cd $OUT && sha256sum -c MANIFEST.sha256 >/dev/null 2>&1)"
  check "bayes_pooled note rows when bayesmeta absent" "Rscript -e 'quit(status = as.integer(requireNamespace(\"bayesmeta\", quietly = TRUE)))' || grep -q 'bayesmeta not installed' $OUT/bayes_pooled.csv"
  n_indiv=$(tail -n +2 "$OUT/freq_individual.csv" | wc -l)
  n_pooled_est=$(python3 -c "
import csv; print(sum(1 for r in csv.DictReader(open('$OUT/freq_pooled.csv')) if r['est'] != 'NA'))")
  if [ "$cfg" = dryrun ]; then
    check "dry-run: 5 individual rows (got $n_indiv)" "[ $n_indiv -eq 5 ]"
    check "dry-run: 0 pooled estimates (got $n_pooled_est)" "[ $n_pooled_est -eq 0 ]"
    check "dry-run: 5 freq_pooled rows all k<3 noted" "[ \$(grep -c 'k<3' $OUT/freq_pooled.csv) -eq 5 ]"
    check "dry-run: measures SMD, SMCR x2, PLO, Z present" "[ \"\$(tail -n +2 $OUT/effect_sizes.csv | cut -d, -f8 | sort | uniq -c | awk '{print \$2\"=\"\$1}' | paste -sd' ')\" = 'PLO=1 SMCR=2 SMD=1 Z=1' ]"
    check "dry-run: placeholder r labelled in derivation" "grep -q 'R_PREPOST_DEFAULT: placeholder pending the statistician' $OUT/effect_sizes.csv"
    check "dry-run: SoF has 5 individual rows with GRADE empty note" "[ \$(grep -c ',individual,' $OUT/summary_of_findings.csv) -eq 5 ]"
  else
    for ab in A03 A07 A05 A21; do
      check "pooling: pooled estimate for $ab" "python3 -c \"
import csv,sys; sys.exit(0 if any(r['ability_id']=='$ab' and r['est']!='NA' for r in csv.DictReader(open('$OUT/freq_pooled.csv'))) else 1)\""
    done
    check "pooling: Egger row for A05" "grep -q '^A05,' $OUT/freq_egger.csv"
    check "pooling: funnel PNG for A05" "[ -s $OUT/funnel_A05_SMD.png ]"
    check "pooling: forest PNGs for the pooled units" "[ -s $OUT/forest_A03_SMD.png ] && [ -s $OUT/forest_A07_SMCR.png ] && [ -s $OUT/forest_A21_PLO.png ] && [ -s $OUT/forest_A05_SMD.png ]"
    check "pooling: Z pooled for A03 (verified population SD)" "grep -q '^A03,Z,' $OUT/freq_pooled.csv"
    check "pooling: non-primary row reported individually, not pooled" "grep -q ',no,' $OUT/effect_sizes.csv && [ \$(python3 -c \"
import csv; print(sum(int(r['k']) for r in csv.DictReader(open('$OUT/freq_pooled.csv')) if r['ability_id']=='A03'))\") -eq 10 ]"
    check "pooling: SE-reported row converted (derivation)" "grep -q 'se\*sqrt(n)' $OUT/effect_sizes.csv"
    check "pooling: prepost sensitivity at r=0.3 and 0.7" "grep -q ',0.3,' $OUT/freq_prepost_sensitivity.csv && grep -q ',0.7,' $OUT/freq_prepost_sensitivity.csv"
    check "pooling: sensitivity rows (fixed_effect, exclude_n_i_le_3)" "grep -q fixed_effect $OUT/freq_sensitivity.csv && grep -q exclude_n_i_le_3 $OUT/freq_sensitivity.csv"
    check "pooling: PLO natural-scale columns filled" "python3 -c \"
import csv,sys; rows=[r for r in csv.DictReader(open('$OUT/freq_individual.csv')) if r['measure']=='PLO']; sys.exit(0 if rows and all(0<float(r['est_natural'])<1 for r in rows) else 1)\""
    check "pooling: SoF joined GRADE on ability_id + outcome" "grep -q 'A03,axillary temperature rise,SMD,5,pooled' $OUT/summary_of_findings.csv && grep -q 'Moderate' $OUT/summary_of_findings.csv"
    check "pooling: LOO rows written" "[ \$(tail -n +2 $OUT/freq_loo.csv | wc -l) -ge 24 ]"
  fi
  echo "  log: $SYN/run_$cfg.log"; grep -E '^(Loaded|Effect sizes|Frequentist|Bayesian|Summary|Rebuilt|Warning|Error)' "$SYN/run_$cfg.log" | sed 's/^/    /'
done
echo "== synthetic tests: $fails failure(s)"
[ $fails -eq 0 ]
