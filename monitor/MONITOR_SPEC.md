# Weekly monitor — specification (created only after Gate 1 is set to Approved)

Purpose: rerun the registered search terms for new records and confirm that every DOI in the master reference list still resolves; post a digest. It never changes a data file.

Schedule: weekly, Monday 06:00 America/Los_Angeles, from Gate 1 approval to Gate 7 submission.
Inputs: searches/registered_strings.md (frozen at Gate 2); extraction/master_references.csv; the record set in screening/.
Steps:
1. Run each registered string against the free APIs only (PubMed E-utilities, Europe PMC REST, OpenAlex, medRxiv/bioRxiv API, and the ClinicalTrials.gov API v2 for registered trials), restricted to records added since the last run. Institutional databases (Embase, PsycINFO, Scopus, if a co-author's institution provides them) are not touched by the task.
   Registered sources and the monitor (charter decision 5 registers PubMed, Europe PMC, OpenAlex, CENTRAL via the Cochrane Library, ClinicalTrials.gov and preprint servers), stated explicitly:
   - **ClinicalTrials.gov is registered and IS monitored**, through its free API v2 (no account needed); new registrations and results postings matching a registered string are listed in the digest like any other record.
   - **CENTRAL is registered but is NOT monitored** by this task, because querying CENTRAL needs Cochrane Library access, which the task does not have. CENTRAL is searched by hand (Sean or a co-author with access) at the registered search date and at any update Sean approves; the digest carries the line "CENTRAL: not monitored (Cochrane Library access required); last manual search <date>" so the gap is visible every week.
2. Deduplicate against the existing record set by DOI, then by normalised title; write new records to searches/alerts/<date>.csv with the string that found each.
3. Resolve every DOI in master_references.csv through Crossref in batches of ten with a two-second pause; list any DOI that no longer resolves or whose title no longer matches.
4. Write the digest to gate-packages/monitor/<date>.md: new records (count and titles), DOI failures, API errors, run trace id.
5. Log the run with traces/trace_logger.py (role `monitor`).
Failure handling: on any API error the step is retried once after 60 s; persistent failure is reported in the digest, not silently skipped. The task never screens or includes a record; new records enter screening only when Sean approves an update at the next gate.
Approval: this specification is a line item at Gate 1. The scheduled task is created after the dropdown shows Approved and not before; nothing is scheduled in Stage 1 (charter standing condition).
