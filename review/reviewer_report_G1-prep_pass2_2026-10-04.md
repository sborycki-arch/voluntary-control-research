# Reviewer report — Gate 1 preparation, pass 2 (2026-10-04)

Reviewer: independent reviewer/PM, role `reviewer`, trace `s1-reviewer-single-20261004T044206Z-3686` (pass 1: `s1-reviewer-single-20261004T042044Z-2d52`, completed).
Scope of this pass: the Stage 1 package (PKG, unchanged since pass 1; tree re-verified identical to the delivered zip) re-reviewed against the inputs Sean uploaded (INPUTS): the Claude Research Team Plan (markdown export), the research document (with the 98-reference list and the Verification status table), the evidence map, the scored dataset and baselines, evidence.py, CLAUDE.md, the repo README, GATE_LOG.md and the skills placeholder. INPUTS/viz was not read (out of scope). The live plan document was not opened by the reviewer; its tracker state is taken from the head agent's report and marked as such.
Environment: as pass 1, plus scipy 1.17.1 installed in a venv under PM/scratch for one check (P60). R 4.3.3 with metafor via apt; CRAN, bayesmeta and meta unavailable; every scholarly host blocked. Nothing under PKG or INPUTS was edited; the only writes under PKG are the two reviewer trace records in traces/stage1.jsonl (and the removal of a `__pycache__` folder the reviewer's own compile check had created, disclosed in section 12).
Issue ids (R-nnn) refer to PM/issues_register.csv (pass-2 rows carry source `reviewer-pass2`); claim ids (Pnn) to PM/claims_audit_pass2.csv; pass-1 claim ids (Cnn) to PM/claims_audit_pass1.csv.

## 1. FAIL list

New in pass 2 (blocker or major). Location | expected | found.

| Id | Location | Expected | Found |
|---|---|---|---|
| R-043 (blocker) | INPUTS/gates/GATE_LOG.md:7,18-23; plan lines 17, 73; CLAUDE.md:11; PKG/gate-packages/G0_2026-10-03_charter-decisions.md:3-4 | Gate 0 set to Approved in the tracker before Stage 1 work starts (plan operating principle; CLAUDE.md gate rule) | GATE_LOG.md reads "Awaiting approval" with six unticked boxes (read by the reviewer); the live plan reads the same per the head agent (not opened by the reviewer); the charter record claims approval "in the project conversation". The Stage 1 package was built without the tracker showing approval. Only Sean resolves this |
| R-044 | plan line 98; INPUTS/skills/README.md:9; appraisal SKILL.md:17 | Appraisal skill contains the RoB 2, ROBINS-I and JBI item lists with GRADE prompts | Item lists not reproduced; skill points to riskofbias.info, jbi.global and gdt.gradepro.org, all unreachable from this environment; versions not pinned |
| R-045 | plan line 60; appraisal SKILL.md:8,30; charter D4 | Two raters assess every study; disagreements go to Sean | Dual rating only "when the head agent asks"; adjudicator is the SME co-author (charter) — a package-vs-plan and a charter-vs-plan departure |
| R-048 | CLAUDE.md:25-31; GATE_LOG.md:26; plan line 112; both README.md files | One repository layout | Gate packages: repo directories `gates/packages/G<n>-<date>/` vs package files `gate-packages/G<n>_<date>_<title>.md` (the plan's wording matches the package); two trackers plus the charter record; two root READMEs; traces/, reporting/, monitor/, dry-run/, schema/ absent from the repo map |
| R-049 | CLAUDE.md:23,28; setup.R:3; charter SC1 | Pilot code and review code separable | Repo analysis/ holds evidence.py (must keep running per CLAUDE.md rule 8); package setup.R runs renv::init in the same analysis/ folder |
| R-050 | CLAUDE.md:16,27; 00_load.R:3; charter SC1 | One rule for where review data lives, with pilot data quarantined | CLAUDE.md says values enter data/ only with row-level provenance; data/ holds pilot files without it; the package reads extraction/master_reconciled.csv and schema/ |
| R-058 | charter D3; METHODS_PAPER_OUTCOMES.md:3; plan lines 83, 110; research-project.md:287 | Every manuscript in the charter has a basis in the plan | The methods paper and its pre-specified outcomes exist only in the charter record and the package; the plan ends at one review manuscript and the research document lists three papers plus a lay article |

Re-graded in pass 2: R-009 (no raw-to-effect-size code) from blocker to major. The plan places the analysis code with the statistician agent at Stage 5 (plan lines 42, 106) and the G1 acceptance criterion is reproduction of the research document's numbers by re-extraction; the package's SCHEMA.md, run_all.R header and dry-run pass criterion 5 still claim more than exists. Sean decides whether a functional rebuild is a Gate 1 requirement.

Pass-1 FAILs still open: R-001, R-003, R-004, R-006, R-007, R-009, R-010, R-012, R-013, R-019, R-020, R-028, R-029 (updated: candidate values verified; access still unconfirmed), R-033, R-034, R-038.
Closed in pass 2 on the reviewer's own verification: R-039 (folder structure matches the plan's list), R-042 (known tool limits verified against plan line 125).
New minor findings (not gate-blocking): R-046, R-047, R-051–R-057, R-059–R-067.

## 2. Unverified list

| Claim | Source | Where tried / why not |
|---|---|---|
| P48 live plan tracker shows G0 "Awaiting approval" (rev 12) | claude.ai/code/artifact/8523b47c-… | Not opened by the reviewer; reading it needs a connector the reviewer's rules exclude. Reported by the head agent; Sean to confirm |
| All pass-1 external items (C40, C44–C57, C59–C72, C74) | standards, tool documents, papers | Still blocked (egress). Partial relief: the research document now supplies every candidate's DOI and the pilot values, so the targets are verified against the document, not yet against the papers |
| Full texts of the seven dry-run candidates | publisher/PMC | Not staged; access unconfirmed for six of seven |

## 3. Checklist table

Unchanged from pass 1: PRISMA-trAIce and Ding Table 10 can still be applied only against the package's paraphrase (R-033, R-034). The plan itself names only PRISMA 2020 for the reviewer skill (plan line 98) and BARG for Method 3; PRISMA-trAIce, RAISE and Ding entered through the charter's Stage 1 additions (R-061). Trace completeness (reviewer step 5): not met (R-001, R-004, R-007); two reviewer records now exist, both with skill_version `no_git`.

## 4. Counts

Pass 2: claims audited 69; verified 47 (46 direct, 1 by reading); mismatched 21; not opened 1.
Cumulative (pass 1 + pass 2): claims audited 155; verified 80; mismatched 40; not opened 35.
Register after pass 2: 67 findings (1 blocker, 22 major, 44 minor); 65 open, 2 closed; open FAILs (blocker or major) 23.

## 5. Judgment

`open failures: 23` (1 blocker, 22 major). The precondition for any Gate 1 submission, Gate 0 Approved in the tracker, is not met (R-043). The package remains not ready to enter a Gate 1 package.

## 6. Plan vs charter record

Where the charter record (G0_2026-10-03) departs from the plan as exported, or the plan departs from itself:

| # | Plan | Charter record | Status |
|---|---|---|---|
| 1 | Six Gate 0 decisions (plan lines 148-153; GATE_LOG six boxes) | Seven: adds Registration (D2) | Documented addition in the charter (line 5); GATE_LOG lacks the seventh (R-061) |
| 2 | Scope: all 26 or lever-free only | All 26; lever-free deferred to G8; k >= 3 pooling, k < 3 individual intervals + Bayesian + GRADE narrative | Consistent with plan Methods 2-3 (P07, P08, P51); individual intervals missing in code (R-010) |
| 3 | Journal tier only | Names Psychophysiology / Autonomic Neuroscience and a second manuscript, the methods paper, to RSM or JCE | Methods paper has no basis in the plan or the research document (R-058) |
| 4 | Co-authors: statistician signs the analysis plan; SME for the primary study; RoB disagreements go to Sean; no human-coded subset | Both co-authors code a blind 10-20% subset for screening and extraction kappa; SME adjudicates RoB 2 and signs GRADE | Charter extends the plan (R-060) and changes the adjudicator (R-045) |
| 5 | Databases: Embase/PsycINFO/WoS vs PubMed/Scopus/Google Scholar; research document protocol: PubMed, Embase, PsycINFO, WoS + Google Scholar | PubMed, Europe PMC, OpenAlex, CENTRAL, ClinicalTrials.gov, preprints; Embase/PsycINFO/Scopus conditional | Three lists (R-059) |
| 6 | Priors: defaults or statistician-set | Defaults stand until the statistician sets them; locked at G5 | Consistent (P07) |
| 7 | Monitor after G1; workflows at G3/G4 | Not approved at G0; line items at G1/G3/G4 | Consistent (P14) |
| 8 | Stage 1 hand-over: skills, schema, environment manifest, dry-run report | Adds monitor specification; adds traces, reporting plan, methods-paper outcomes | Additions (R-061); README carries all |
| 9 | Pre-registration on PROSPERO before screening | PROSPERO with OSF fallback; after G2 | Consistent; fallback added (P13) |
| 10 | Standing condition 1: pilot is rationale only | Research document H7 compares against the pilot correlation | Tension to resolve at G2 (R-063) |
| 11 | Plan-internal: "Eight gates" vs "Nine gates"; "registered criteria" at Stage 1 before G2 registration | — | R-062, R-066 |
| 12 | Gate passes only when Sean sets Approved in the Section 5 tracker | "Approved 2026-10-03, in the project conversation"; dropdown "set by Sean" | Tracker not set (R-043) |

## 7. Package vs plan (Stage 1 paragraph, G1 row, team table, three methods, quality controls, tool limits, CLAUDE.md)

Verified consistent: dry-run requirement quotation (P01); G1 deliverable list (P02); folder structure (P03); known tool limits (P04, P05); Method 2 implementation in 01_frequentist.R except effect-size derivation and k < 3 intervals (P51, P52); Method 3 by reading (P53); provenance fields and refusal (P56); monitor deferral (P57); gate-package parts (P58); pin list (P63); hand-over chain (P66); environment wording (P67); skills layout (P49).
Departures, package from plan: appraisal item lists absent (R-044); dual rating optional (R-045); RoB items excluded from extraction (R-046); screening uses DRAFT criteria where the plan says registered (R-066, plan-internal); `meta` pinned but unused (R-067).
Departures, package from CLAUDE.md: Stage 1 built while G0 is "Awaiting approval" (R-043); data location and provenance rule (R-050); repository map (R-048); rule 5 vs the reviewer skill's snippet rule (R-065). CLAUDE.md's style rule ("at most one question, at the end") does not fit a reviewer report's open-questions section; the report format follows the reviewer skill.

## 8. Dry-run candidates against the research document

| Candidate | Pilot value quoted correctly | In Verification status table | Notes from the document | Qualifies under rules (a)-(d) |
|---|---|---|---|---|
| Kozhevnikov 2013 (A03) | Yes (P17) | No (P24) | 2.2 degC participant 3; 38.30 degC participant 5; open access (PLoS ONE) | Yes; the only candidate with confirmed access |
| Zeidan 2011 (A10) | Yes (P18) | No (P25) | n = 15, no sham; ROBINS-I for an uncontrolled pre/post is an SME question (R-023) | Yes, subject to access |
| Meissner 2024 (A08) | Yes, as a count (P19) | No (P26) | Target should be the measured values (F, eta-p2, 27/27 analysed) (R-053) | Yes, subject to access |
| Code 1995 (A21) | Yes (P20) | No (P27) | 22% / 18%, n = 442 | Yes, subject to access |
| Eberhardt 2021 (A06) | Yes (P21) | No (P28) | "about 2.4 mm" / "about 0.8 mm"; printed precision needs the paper (R-054) | Yes, subject to access |
| Manuck 1976 (A14) | Yes (P22) | No (P29) | Four conditions x 15; randomisation not stated; tool to be chosen from the paper (R-053) | Yes with the design caveat, subject to access |
| Paravlic 2018 (A12) | Yes (P23) | No (P30) | Meta-analysis: `harvest` under the package's own rules; not extracted or appraised (R-052) | As a screening `harvest` test only |

Rule (a) as written refers to a "verified status" the document does not have; the document lists only the 26 sources with gaps (R-051). Applied as "not in that table", none of the seven is excluded. Which five are chosen is the builder's and Sean's decision; the reviewer notes that a set covering RoB 2, ROBINS-I, JBI case report and JBI prevalence needs Meissner (or Manuck), Kozhevnikov and/or Zeidan, Eberhardt and Code, and that only Kozhevnikov's access is confirmed today.

## 9. population_sd.csv against baselines.csv and the research document

All seven rows match cell for cell on mean, SD, unit and n where given (P33-P39). Discrepancies: four DOIs present in the research document are blank in the csv; the finger-temperature note "(identify exact paper)" is stale (document: Gatt et al. 2019, DOI given); the hearing SD is "approximately 5 (model estimate about 4)" in the document but 5.0 flat; sample descriptors (551 measurements; 51 controls; 91 eyes) not carried (R-055). The repo's own baselines.csv and evidence.py carry the stale "Sci Rep 2019" form (R-056, for Sean). All rows are pilot_unverified and excluded by 00_load.R (executed in pass 1).

## 10. abilities.md against evidence.csv

Same set: 26 to 26, one-to-one by name (P43); names paraphrased, codes A01-A26 not present in evidence.csv and ids not present in abilities.md, so the crosswalk is undocumented; no key sources in abilities.md to compare (P45, R-057). Exclusions match (P44).

## 11. Repository integration: conflicts and the decisions only Sean can make

Conflicts (no merge proposed): (1) gate-package location and naming; (2) authoritative tracker (GATE_LOG.md, the live dropdown, or the charter record); (3) analysis/ holds pilot Python and would hold the review R scaffold plus renv files; (4) data/ (CLAUDE.md) vs extraction/ and schema/ (package), and pilot data without row-level provenance under a rule that requires it; (5) two root READMEs; (6) traces/, reporting/, monitor/, dry-run/, schema/ not in the repo map or CLAUDE.md; (7) CLAUDE.md's gate rule would apply to any session on the merged tree, so the authority question (R-043) precedes the merge. Decisions for Sean: D-i which tracker is authoritative and set it; D-ii one gate-package convention; D-iii folder split for pilot vs review code and data, honouring SC1; D-iv repository map and CLAUDE.md revision to carry the package's additional folders; D-v whether the G0 record needs the four-part package form (R-047).

## 12. Reviewer's own deviations and environment changes (disclosed)

- `python3 -m py_compile` on PKG/traces/trace_logger.py in pass 1 created PKG/traces/__pycache__/ (my artefact, not package content). I removed it and re-verified the tree against the delivered zip: identical apart from the two permitted trace writes and the pass-1 prompt file the head agent placed. The repo's .gitignore would have excluded it; the package has no .gitignore.
- scipy 1.17.1 was installed in a venv under PM/scratch to run evidence.py once (P60). No system Python was changed.
- R 4.3.3 and packages were installed by the head agent via apt (not by the reviewer); the reviewer used them on scratch copies only. This is not the pinned environment.

## 13. Open questions for Sean

1. Gate 0 authority (R-043): will you set G0 to Approved in GATE_LOG.md and the live tracker, confirming the charter record, or return it? Which tracker is authoritative?
2. Methods paper (R-058): is it in scope? If yes, the plan needs amending (writer, reviewer, G7, registration supplement).
3. Appraisal item lists (R-044): accept the package's URL-only approach, or require the lists in the skill as the plan says?
4. Dual rating and adjudicator (R-045): every study by two raters with your adjudication (plan), or optional dual rating with SME adjudication (package/charter)?
5. RoB items in extraction (R-046): accept the package's separation?
6. Database list (R-059): which of the three lists goes into the G2 protocol?
7. Blind subset (R-021, R-060) and extraction kappa (R-020): who codes it, and is extraction kappa required?
8. Repository integration decisions D-i to D-v (section 11).
9. Environment route (R-038): CRAN-reachable machine with renv; apt R with brms for Method 3; or Python (the plan allows either). Is the project under git before the first dry-run call (R-004)?
10. Does the Stage 1 scaffold need a working raw-to-effect-size step at Gate 1 (R-009), or is that Stage 5 as the plan says?
11. Dry run under D7 (R-027): skill test or workflow?
12. The build run's missing trace (R-001): retroactive record acceptable?
13. Can the standards' primary texts and the seven full texts be uploaded (S5, S7)?

## 14. Not audited / limits of this pass

- The live plan document and its revision history were not opened by the reviewer.
- No external source was opened; the candidates' values are verified against the research document, not the papers.
- INPUTS/viz was not read.
- The research document's 98 references were counted, not individually checked against Crossref (blocked).
- 02_bayesian.R, run_all.R and setup.R remain read-only reviewed.

## Addendum (pass 3, builder items adjudication, 2026-10-04)
Ten builder review items were verified against the package and added to the register as R-068 to R-077 (source=builder; details and evidence in PM/builder_items_adjudication.md). R-058 was re-worded (plan not amended for a charter addition) and lowered to minor. New FAILs: R-068, R-069, R-070, R-071, R-075, R-076, R-077. Updated judgment: `open failures: 29` (1 blocker, 28 major). Trace: s1-reviewer-single-20261004T112327Z-5788 (run 2; run 1 discarded after a platform rate limit).
