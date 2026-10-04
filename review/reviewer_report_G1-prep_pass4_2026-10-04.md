# Reviewer report — Gate 1 preparation, pass 4: re-review of the round-2 build (2026-10-04)

Reviewer: independent reviewer/PM, role `reviewer`, trace `s1-reviewer-single-20261004T130638Z-1730` (parent: pass-3 run 2). Review target: BUILD = scratchpad/vcr-build at commit e846498 (baseline d6306f3 = the delivered zip; contract 66351bd). Reference for "as delivered": scratchpad/vcr (unchanged). Every execution was on a scratch extract of e846498 (`git archive`) under PM/scratch, never in BUILD; the only write under BUILD is this run's trace record. The builder side's own verification (build-log/VERIFY_A–D, VERIFY_INTEGRATION) was read but not relied on: every closure below was re-verified by the reviewer's own execution or reading, as the `verified_by` column of issues_register.csv records.
Environment: R 4.3.3, metafor 4.4.0 (system library); bayesmeta and meta absent; CRAN and all scholarly hosts blocked. Python 3.11.
Issue ids (R-nnn) refer to PM/issues_register.csv; claim ids (Q-…) to PM/claims_audit_pass4.csv.

## 1. FAIL list (blocker or major rows not closed after this pass)

| Id | Status | Location | Expected | Found after round 2 |
|---|---|---|---|---|
| R-043 (blocker) | open | GATE_LOG.md; live plan | Gate 0 shown Approved in a tracker | Sean's session statement reported; live plan read Awaiting at rev 12; static GATE_LOG export reads Awaiting. Not observed Approved |
| R-001 | partial | traces/stage1.jsonl record 8 | Trace of the build run | Retroactive record only (verified: zip hash and 20/20 member hashes); agent_role `head` contradicts its own stand-in prompt; refs are absolute paths outside the package; acceptance is Sean's |
| R-007 | partial | TRACE_SPEC.md; traces/transcripts/ | Transcript per run | Mechanism works (tested); zero transcripts attached for 16 runs; procedure names no file location although 11 platform transcript files are visible under the session's subagents folders (names only; not read) |
| R-012 | partial | 02_frequentist.R; 04_sof.R | Granularity rule end to end | Pooling unit and SoF join fixed (executed); dependent-effect-size aggregation is a G5 decision |
| R-020 | partial | extraction SKILL.md; METHODS #4 | Extraction agent-vs-human κ per charter D4 | Blind subset procedure and agreement rates specified; κ requirement is Sean's |
| R-029 | open | DRY_RUN_PROTOCOL.md | Five candidates with full text | Only Kozhevnikov access confirmed; selection.csv header-only |
| R-033, R-034 | open | reviewer checklists | Published item lists | Unreachable; templates header-only |
| R-038 | open | ENVIRONMENT.md | Pinned environment | Route undecided; scripts run on system R; setup.R unexecutable here |
| R-044, R-045, R-048, R-049, R-050, R-071 | open | skills; repo layout; methods paper | Sean/SME decisions | Unchanged by design (contract scope) |
| R-068 | partial | screening SKILL.md:32,40 | Scope ruling on validated self-report outcomes | Criteria redrafted to admit them (builder action under the contract's exception); Sean's G2 confirmation pending |
| R-076 | partial | run_all.R; setup.R | Pinned library used; brms fallback | (a) executed: unrestored lockfile stops the run; positive path unexecutable here; (b) by reading |

Closed this pass on the reviewer's own verification (34): R-002, R-003, R-004, R-005, R-006, R-008, R-009, R-010, R-011, R-013, R-014, R-017, R-018, R-019, R-022, R-024, R-026, R-028, R-030, R-031, R-051, R-052, R-053, R-054, R-055, R-057, R-064, R-067, R-069, R-070, R-072, R-073, R-075, R-077.
New minor findings this pass: R-078 (logger/spec residuals incl. cwd-dependent skill_version), R-079 (agent commits authored as Sean), R-080 (ENVIRONMENT.md "every script" overstatement), R-081 (head agent's prompt not stored), R-082 (row-numbering conventions), R-083 (verifier residuals left open).

## 2. Unverified list
| Claim | Where tried / why not |
|---|---|
| Sean's "G0 set to Approved in both trackers" | Reviewer has no connector access to the live plan; the only GATE_LOG copy available is the 04:15Z upload (Awaiting). Head agent's live read at rev 12 also Awaiting |
| The present-bayesmeta branch of 03_bayesian.R (summary indexing, k = 1 fit, Bayes factor) | bayesmeta not installable; VERIFY_B's stub run not reproduced |
| setup.R end to end (renv snapshot, brms fallback) | CRAN blocked; parse and reading only |
| Positive renv path (a restored project library in use) | cannot restore here |
| All pass-1/2 external sources (standards, papers) | still blocked; unchanged |

## 3. Checklist table (PRISMA-trAIce paraphrase; Ding Table 10 paraphrase; trace completeness)
| Item | Status after round 2 | Evidence |
|---|---|---|
| Tool identity and version | met in specification | model string in every live record; `not_recorded` only in the retroactive one |
| Stage of use | met in specification | REPORTING_PLAN disclosure (updated for the blind extraction subset) |
| Prompts and configuration | partly met | 15 prompt files stored and hash-verified 16/16; the head agent's own round-2 prompt is the contract file, not the instruction received (R-081) |
| Validation performed | cannot be checked before the dry run | synthetic suites pass; no real paper processed |
| Human oversight | met in specification; still no consolidated HITL list | skills, charter, OPEN_DECISIONS |
| Error handling | met | loader refusals executed; logger exit-2 paths tested; safety_stop_subject field |
| Limitations | met | README known limits now carry the research document's full access-failure list |
| Ding: HITL entry points stated as a list | not met | still scattered |
| Ding: code released (runnable) | partly met | scaffold runs end to end on synthetic data in this container; not pinned |
| Ding: seeds/execution traces released | partly met | locked logger, 16 records, prompts stored; zero transcripts; one retroactive record |
| Ding: novelty-verification method | not applicable at G1 | Stage 2 |
| Ding: attempts and selection policy | met in specification | run_number/selection_policy validated; discarded runs closed (reviewer run 1 of pass 3) |
| Reviewer step 5: every run has a complete record with model, skill version, inputs, outputs, selection | partly met | 15/15 prior records complete; retroactive record lacks model/skill; integration verifier record skill_version not_recorded (R-078c); reviewer records no_git (R-078a) |

## 4. Counts
Claims audited this pass: 83; verified 78; mismatched 4; not opened 1.
Register after pass 4: 83 rows (1 blocker, 28 major, 54 minor); status closed 36, partial 11, open 36. Rows not closed by severity: blocker 1, major 16, minor 30.

## 5. Judgment
`open failures: 17` (1 blocker; 16 major, of which 6 partial and 10 open majors). Down from 29 after pass 3. Every builder-owned closure claim held under re-verification except where graded partial above; no regression that breaks execution was found. The package still cannot enter a Gate 1 package: the precondition (R-043) is unmet and the remaining FAILs are decisions and inputs owned by Sean, the SME or the statistician, plus the environment pin and the dry run itself.

## 6. Executions performed by the reviewer (all on scratch copies)
- `bash analysis/synthetic/run_synthetic_tests.sh`: exit 0, 51 ok (both configurations). `python3 traces/test_trace_logger.py`: exit 0, 45 ok.
- Deliberately broken masters through run_all.R: blank location, missing doi+url → provenance refusal with REFUSED csv; blank is_primary_outcome, lever_type 'hands', design 'case-study' → vocabulary refusal with reasons; abstract_only → provisional stop; blank n_total → passes (only the column is required). Checkout without analysis/outputs/: refusal and file written.
- Two consecutive pooling runs: MANIFEST.sha256 byte-identical (CSV and PNG); manifest excludes itself; inputs not in the outputs folder.
- reconcile.py: diff (5 discrepancies, all five types), build refused with an empty log (nothing written), build with full log and primary file → loads in 00_load.R (7 rows); build without --primary → loader refuses all rows.
- 04_sof.R: GRADE file absent → exit 0 with note; zero effect sizes with GRADE present → exit 0, header-only inputs file.
- Stub unrestored analysis/renv.lock → run_all.R stops with the plain remedy; VCR_IGNORE_RENV=1 announces the bypass.
- Independent recomputation of the dry-run SMD, SMCR, PLO and Z effect sizes (metafor::escalc; SCHEMA delta-method): 4/4 match to 1e-6.
- Logger races against the new logger: 60 concurrent ends → record complete, 0 failures (59 overwrite warnings); 3 × 20 interleaved start→end pairs → 20/20/0 torn/0 errors each.
- Trace audit: 16 records; my four earlier records byte-identical to the PKG copy; 16/16 prompt hashes match; retroactive record 20/20 + zip hash; stage file mode 644; `check --stage 1` lists only my open pass-4 record.
- Standalone scripts from analysis/: 00_load.R and run_all.R give the plain message; 01/02/04 do not (R-080).

## 7. Regression hunt
No file outside the ownership union was touched (git diff 66351bd e846498 --name-only against BUILD_CONTRACT.md). Found: (i) prose overstatement ENVIRONMENT.md:4 (R-080); (ii) fixer changelogs moved from the package root to build-log/ by the head agent against contract item 9 (harmless; CHANGELOG.md and README say build-log/); (iii) the head agent's six commits are authored as Sean with identical 13:05 timestamps (R-079); (iv) the head agent's run record uses the contract as its prompt (R-081); (v) VERIFY_INTEGRATION's ten inconsistencies: items 1–9 fixed in d236a42 (each re-read or executed), item 10 (synthetic extractor_id outside the vocabulary) not, carried in R-083; (vi) the k_ability and as_number residuals from VERIFY_B/C not addressed (R-083). Nothing the round changed broke the loader, the synthetic suite, the logger or the reconciliation tool.

## 8. Builder actions awaiting Sean's confirmation
- R-021: skills/screening/SKILL.md:48 now reads "the two human co-authors ... screen that subset blind ... Sean adjudicates ... and therefore does not code the subset" (charter D4 wording). Changed by fixer C although the row is Sean's; disclosed in CHANGELOG.md and OPEN_DECISIONS.md.
- R-068: the DRAFT Outcome bullet and E3 admit validated pain ratings and seizure diaries, labelled "confirm at G2 (R-068)". Changed under the contract's stated exception; the scope ruling remains Sean's.
Both stay non-closed in the register until Sean confirms or returns them.

## 9. Trace audit
16 records (15 before this pass). Reviewer passes 1–3 (four records incl. the discarded run 1) byte-identical to the PKG copy. Head agent round 2, four fixers, five verifiers: all complete, selection single_run, retroactive false, transcript_kind none. Retroactive build record: retroactive true, model/skill not_recorded, agent_role `head` although its stand-in prompt says a separate builder agent built the package, refs absolute and outside the package (R-001 partial, Sean's acceptance). Integration verifier: skill_version not_recorded for a nonexistent --skill path (R-078c). Head agent record: prompt_ref and skill = BUILD_CONTRACT.md (R-081). My pass-4 record: skill_version no_git because the logger derives it from the caller's cwd (R-078a); I cannot edit it. Zero transcripts for any run (R-007).

## 10. What still blocks Gate 1, by owner
- **SME co-author** (2): R-023 (minor, open); R-074 (minor, open)
- **Sean** (27): R-021 (minor, open); R-027 (minor, open); R-029 (major, open); R-032 (minor, open); R-033 (major, open); R-034 (major, open); R-038 (major, open); R-041 (minor, open); R-043 (blocker, open); R-045 (major, open); R-046 (minor, open); R-047 (minor, open); R-048 (major, open); R-049 (major, open); R-050 (major, open); R-056 (minor, open); R-058 (minor, open); R-059 (minor, open); R-060 (minor, open); R-061 (minor, open); R-062 (minor, open); R-063 (minor, open); R-065 (minor, open); R-066 (minor, open); R-068 (major, partial); R-071 (major, open); R-079 (minor, open)
- **builder** (14): R-001 (major, partial); R-007 (major, partial); R-015 (minor, partial); R-020 (major, partial); R-035 (minor, partial); R-036 (minor, partial); R-037 (minor, partial); R-044 (major, open); R-076 (major, partial); R-078 (minor, open); R-080 (minor, open); R-081 (minor, open); R-082 (minor, open); R-083 (minor, open)
- **statistician co-author** (4): R-012 (major, partial); R-016 (minor, partial); R-025 (minor, open); R-040 (minor, open)

Blocking in substance: R-043 (tracker), R-029 (full texts), R-038 (environment route and pin), the dry run itself (not executed), R-001/R-007 (trace acceptance and transcripts), and Sean's rulings on R-021, R-027, R-068, R-044, R-045, R-020. The repository integration decisions (R-048–R-050) block the package's location, not its content.

## 11. Open questions for Sean
1. Confirm R-021 and R-068 as changed, or return them.
2. Accept or reject the retroactive build-run record; should a second retroactive record with role `builder` be written (OPEN_DECISIONS)?
3. Transcript policy: require platform_export from the dry run on? The platform files appear to exist on disk.
4. R-009: is a working raw-to-effect-size step required at G1 (it now exists) or reviewed only at G5?
5. R-030: the protocol reports κ with its CI and makes "every disagreement adjudicated" the acceptance criterion instead of a κ threshold; accept?
6. R-079: commit identity for agent commits.
7. Environment route (R-038) and the machine for the pin; full texts (R-029); primaries (R-033/R-034).
8. Decoys 8–10 (immune-conditioning records) and an E8 test record (fixer D's questions in OPEN_DECISIONS).

## 12. Not audited / limits
- The live plan document was not opened (no connector use by the reviewer).
- The present-bayesmeta branch, setup.R and the positive renv path were not executed (environment).
- Platform transcript files were listed by name and count only; none was read.
- Verifier reports were read for their findings but every verdict used here was re-established by the reviewer's own check.
