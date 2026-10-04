# Voluntary Body Control Research Program

Evidence base, scored dataset, analysis code, visualisations and the stage-gated plan for a research program on deliberate control of normally involuntary bodily functions. Compiled 2026-10-03 in a Claude session; this bundle is the hand-off into Claude Code.

Program lead and sole approver: Sean Borycki. Gate status lives only in the Stage gates table of the live plan (link below); this repository holds no gate status.

## What is here

| Path | Contents |
| --- | --- |
| `CLAUDE.md` | Working rules for Claude Code sessions in this repo: the gate rule, provenance, verification, pacing, style |
| `docs/research-project.md` | Voluntary Body Control Research Project: summary, rubrics, evidence by system with exact figures, quantitative synthesis, verification status, gaps, study protocol, 98 references with DOIs (export of the live Claude Doc; two charts replaced by placeholders) |
| `docs/research-team-plan.md` | Claude Research Team Plan: operating principles, team architecture, the three certainty methods (GRADE; frequentist random-effects; Bayesian hierarchical), gate tracker, roadmap, work plan, quality controls, risks, Gate 0 decisions |
| `docs/evidence-dataset.md` | The scored dataset as a ranked markdown table with rubrics and baseline sources |
| `docs/overviews/` | One-page overviews of each document (also stored in the Huberman Lab Claude Project) |
| `data/evidence.json` | 26 abilities with certainty, prevalence, strength (SD from the mean), band, basis, sources; plus baselines and Spearman statistics |
| `data/evidence.csv` | Flat version of the dataset |
| `data/baselines.csv` | Population means and SDs used for the strength scores, with sources |
| `analysis/evidence.py` | Rebuilds `data/evidence.json`: strength scores, bands, elevation, Spearman ρ (certainty, prevalence) |
| `viz/terrain_template.html`, `viz/build_terrain.py` | Source and build script for the 3D evidence map (Plotly 2.35.2 from cdn.jsdelivr.net); `viz/terrain.html` is the built page |
| `viz/token_drawdown.py` | Session token-usage chart script (reads a Claude transcript); `viz/token_drawdown.png` is the chart from the originating session |
| `gates/GATE_LOG.md` | Pointer to the live gate tracker; gate packages go under `gates/packages/` |
| `skills/` | Placeholder on `main`; the four SKILL.md files and the rest of the Stage 1 package are on branch `stage1-package`, not yet merged |

## Live documents
- Research project (Claude Doc): https://claude.ai/code/artifact/6f9aa87b-3c23-4c5a-a2bf-3b7b0440a3eb
- Team plan with approval dropdowns — the only gate tracker (Claude Doc): https://claude.ai/code/artifact/8523b47c-b760-4bd5-a176-3022f20639c2
- 3D evidence map (artifact): https://claude.ai/artifact/HDVbejcMxEMmH8LBqoiEci

The files in `docs/` are exports of the live documents as of 2026-10-03. Where they differ from the live documents (for example the plan's gate statuses, and its reference to `gates/GATE_LOG.md` as a copy of the tracker), the live documents govern.

## Rebuild
```
pip install -r analysis/requirements.txt
python analysis/evidence.py        # rewrites data/evidence.json, prints Spearman statistics
python viz/build_terrain.py        # rewrites viz/terrain.html and viz/terrain_standalone.html
```
Expected statistics: n = 11, ρ(certainty) = −0.60 (p ≈ 0.05), ρ(prevalence) = −0.81 (p = 0.002).

## Provenance note
Every figure in `docs/research-project.md` was read in the cited source unless its Verification section (Section 10) says otherwise; that section lists the 26 sources resting on secondary accounts or abstracts and the corrections made during reconciliation. DOIs were confirmed against Crossref or publisher pages; entries without a confirmable DOI carry a PubMed ID or URL.
