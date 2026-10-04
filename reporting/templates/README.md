# Checklist templates (header-only)

These three CSVs are the target files for the reporting-standard audits named in reporting/REPORTING_PLAN.md and skills/reviewer/references/checklists.md. They ship with a header line only.

| File | Standard | Header |
|---|---|---|
| prisma2020_checklist.csv | PRISMA 2020 (Page et al. 2021, BMJ 372:n71) | `item, section, description_short, location_in_manuscript, status` |
| prisma_p_checklist.csv | PRISMA-P (Shamseer et al. 2015, BMJ 349:g7647) | `item, section, description_short, location_in_manuscript, status` |
| prisma_traice_checklist.csv | PRISMA-trAIce (JMIR AI 2025, e80247) | `item_id, item_text_verbatim, source_page, location, status` |

## Rule on item texts
The item texts (`description_short`, `item_text_verbatim`) are **copied from the primary documents when they are available** (the published checklist PDF or the journal article's checklist table) and are **not to be reconstructed from memory**, by an agent or by a person. `source_page` records the page or table of the primary document the text was copied from. Until a primary document has been opened and read, the file stays header-only; a row with an item text and no `source_page` is invalid. None of the three primary documents could be opened from the build environment on 2026-10-04 (register R-033, R-037), which is why no rows are shipped.

## Filling
- `item`/`item_id`: the item number as the standard numbers it (for example `10a`), one row per item or sub-item.
- `location_in_manuscript`/`location`: section and page or line range of the manuscript (or protocol) that satisfies the item; blank with `status = not_met` or `not_applicable` otherwise.
- `status` ∈ `met`, `partly_met`, `not_met`, `not_applicable`, `pending`.
- Filled copies live where REPORTING_PLAN.md says (manuscript/, protocol/, reporting/); the templates here are not edited once filled copies exist.
