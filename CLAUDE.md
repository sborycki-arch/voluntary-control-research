# CLAUDE.md — Voluntary Body Control Research Program

This repository holds the evidence base, scored dataset, analysis code, visualisations and the stage-gated plan for a research program on deliberate control of normally involuntary bodily functions. Sean Borycki is the program lead and sole approver.

## Read first
- `docs/research-team-plan.md` — how the team works, the three certainty methods, the gates.
- `docs/research-project.md` — the evidence base, rubrics, verification status, protocol and 98 references.
- `gates/GATE_LOG.md` — current gate status. **Check it before doing any work.**

## Gate rule (non-negotiable)
Work on a stage starts only after its preceding gate is marked `Approved` by Sean in `gates/GATE_LOG.md`. If the gate you need is not Approved, prepare nothing beyond the current stage's deliverable and say so.

Never, without an approved stage naming it: submit a manuscript, register a protocol (PROSPERO/OSF), contact a journal, co-author, institution or participant, spend money, publish anything publicly, create a scheduled task, or start a multi-agent workflow.

## Working rules
1. **Provenance on every number.** A value enters `data/` only with: source DOI or URL, location in the source (page, table, figure), extractor (agent or person), date, and verification route. Rows missing any field are rejected by the analysis code.
2. **Verify, don't recall.** Numbers come from an opened source page, never from memory or a search snippet. What could not be opened is marked unverified in the record, not filled in.
3. **Dual extraction.** Screening and extraction are done twice by independent runs that cannot see each other; disagreements are listed for Sean, never resolved silently.
4. **Adversarial review before every gate package.** A fresh session rechecks every claim against its source and reruns every number from the raw file.
5. **Citation lookups are paced.** Crossref, OpenAlex and publisher pages rate-limit in bursts: query a few at a time with waits. PubMed pages return no content to the fetch tool; do not use them as sources. WebSearch of a bare DOI string is a reliable way to confirm DOI→title.
6. **Rubrics are stated before scores.** Use the definitions in `docs/research-project.md` Section 3 (certainty, strength vs mean, prevalence) or the GRADE / meta-analysis methods in `docs/research-team-plan.md` Section 4. No ad hoc ratings.
7. **Immune-challenge literature** (endotoxin studies) is extracted in the main session with Sean present, not by background agents; keep wording clinical.
8. **Reproducibility.** `python analysis/evidence.py` must rebuild `data/evidence.json` and the Spearman statistics from the inline dataset; `python viz/build_terrain.py` must rebuild `viz/terrain.html`.

## Repository map
- `docs/` — exported documents and overviews.
- `data/` — `evidence.json` (scored dataset), `evidence.csv` (flat), `baselines.csv` (population means/SDs with sources).
- `analysis/` — `evidence.py` (scoring, bands, Spearman); `requirements.txt`.
- `viz/` — 3D terrain map source and build script; session token-usage chart script.
- `gates/` — the gate log Sean edits.
- `skills/` — placeholder; the four SKILL.md files are a Stage 1 deliverable and do not exist until Gate 0 is Approved.

## Style for Sean
Lead with the answer; no preamble or option menus. Direct and factual; challenge him when he is factually wrong. No numeric ratings without a stated rubric; no emoji status markers; no motivational closers. At most one question, at the end, only where the answer genuinely forks — except on anything submitted or sent out, where questions come first.
