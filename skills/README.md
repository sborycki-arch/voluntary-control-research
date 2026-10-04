# Skills

The four skills (screening, extraction, appraisal, reviewer) are the Stage 1 deliverable and are written only after Gate 0 is Approved in `gates/GATE_LOG.md`.

Planned layout (one folder per skill, each with a `SKILL.md`):

- `screening/` — the registered eligibility criteria as a decision list; outputs include/exclude with reason codes.
- `extraction/` — field-by-field extraction into the master CSV schema; the provenance block (DOI/URL, location, extractor, date, verification route) is mandatory.
- `appraisal/` — RoB 2, ROBINS-I and JBI item lists with the GRADE domain prompts (risk of bias, inconsistency, indirectness, imprecision, publication bias; upgrades for large effect, dose-response, opposing confounding).
- `reviewer/` — PRISMA 2020 checklist plus a claims-to-source audit; reports pass/fail per claim and lists what could not be opened.
