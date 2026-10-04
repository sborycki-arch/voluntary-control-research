#!/usr/bin/env python3
"""reconcile.py: diff two independent extractor files and build the reconciled master (Python 3 stdlib only).

Procedure and file layouts: tools/RECONCILIATION.md and schema/SCHEMA.md.

  python3 tools/reconcile.py diff  A.csv B.csv --out discrepancies.csv
  python3 tools/reconcile.py build A.csv B.csv adjudication_log.csv --out master_reconciled.csv
                                   [--primary primary_outcomes.csv] [--date YYYY-MM-DD]

Rows are matched on the five key fields (study_id, ability_id, outcome_measure, condition_label, timepoint).
Every differing field is one discrepancy row: discrepancy_id, key, field, value_A, value_B, type, where type is
missing_in_A | missing_in_B | numeric | text, or provenance for the provenance fields (source_doi, source_url,
location, verbatim_anchor, verification_route). The run-metadata fields extractor_id, extraction_date, skill_version
and model identify the run, not the paper: they are not diffed and are rewritten in the reconciled file
(extractor_id = reconciled; extraction_date = build date; skill_version / model = the common value or A=<a>;B=<b>).
`build` refuses (exit 2, nothing written) while any discrepancy lacks an adjudication-log row, while the log holds a
row for a discrepancy that no longer exists, or while a log row is malformed.
Exit codes: 0 success; 2 validation error or refusal (one message per problem on stderr, nothing written).
"""
import argparse
import csv
import datetime as _dt
import os
import sys

KEY_FIELDS = ["study_id", "ability_id", "outcome_measure", "condition_label", "timepoint"]
PROVENANCE_FIELDS = ["source_doi", "source_url", "location", "verbatim_anchor", "verification_route"]
RUN_METADATA_FIELDS = ["extractor_id", "extraction_date", "skill_version", "model"]
DISCREPANCY_COLUMNS = ["discrepancy_id", "key", "field", "value_A", "value_B", "type"]
LOG_COLUMNS = ["discrepancy_id", "decision", "chosen_value", "adjudicator", "date", "reason"]
PRIMARY_COLUMNS = ["study_id", "ability_id", "outcome_measure"]
KEY_SEP = "|"
ROW_FIELD = "row"


def die(messages, code=2):
    if isinstance(messages, str):
        messages = [messages]
    for m in messages:
        sys.stderr.write("reconcile: " + m + "\n")
    sys.exit(code)


def warn(message):
    sys.stderr.write("reconcile: warning: " + message + "\n")


def read_csv(path, required, label):
    if not os.path.isfile(path):
        die("%s file not found: %s" % (label, path))
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = []
        for i, r in enumerate(reader, start=2):
            if None in r:  # more cells than header
                die("%s %s: line %d has more cells than the header" % (label, path, i))
            rows.append({k: (v if v is not None else "").strip() for k, v in r.items()})
    missing = [c for c in required if c not in header]
    if missing:
        die("%s %s lacks required column(s): %s" % (label, path, ", ".join(missing)))
    return header, rows


def key_of(row, label, line):
    parts = [row.get(k, "") for k in KEY_FIELDS]
    for k, v in zip(KEY_FIELDS, parts):
        if KEY_SEP in v:
            die("%s line %d: key field %s contains '%s', which is the key separator" % (label, line, k, KEY_SEP))
    if parts[0] == "":
        die("%s line %d: study_id is blank" % (label, line))
    return KEY_SEP.join(parts)


def index_rows(rows, label):
    idx = {}
    problems = []
    for i, r in enumerate(rows, start=2):
        k = key_of(r, label, i)
        if k in idx:
            problems.append("%s: duplicate key on line %d (first seen line %d): %s" % (label, i, idx[k][0], k))
        else:
            idx[k] = (i, r)
    if problems:
        die(problems + ["%s: key fields (%s) must be unique within one extractor file" % (label, ", ".join(KEY_FIELDS))])
    return {k: v[1] for k, v in idx.items()}


def as_number(s):
    t = s.replace(",", "") if s.count(",") and s.replace(",", "").replace(".", "", 1).lstrip("-").isdigit() else s
    try:
        return float(t)
    except ValueError:
        return None


def classify(field, a, b):
    """Return the discrepancy type for two differing, non-identical values, or None if they are equivalent."""
    if a == b:
        return None
    if field in PROVENANCE_FIELDS:
        return "provenance"
    if a == "" and b != "":
        return "missing_in_A"
    if b == "" and a != "":
        return "missing_in_B"
    na, nb = as_number(a), as_number(b)
    if na is not None and nb is not None:
        return None if na == nb else "numeric"
    return "text"


def compute_discrepancies(header_a, rows_a, header_b, rows_b):
    idx_a = index_rows(rows_a, "A")
    idx_b = index_rows(rows_b, "B")
    fields = [c for c in header_a if c not in KEY_FIELDS and c not in RUN_METADATA_FIELDS]
    fields += [c for c in header_b if c not in header_a and c not in KEY_FIELDS and c not in RUN_METADATA_FIELDS]
    out = []
    for k in sorted(set(idx_a) | set(idx_b)):
        in_a, in_b = k in idx_a, k in idx_b
        if in_a and not in_b:
            out.append({"key": k, "field": ROW_FIELD, "value_A": "row present", "value_B": "", "type": "missing_in_B"})
            continue
        if in_b and not in_a:
            out.append({"key": k, "field": ROW_FIELD, "value_A": "", "value_B": "row present", "type": "missing_in_A"})
            continue
        ra, rb = idx_a[k], idx_b[k]
        for f in fields:
            a, b = ra.get(f, ""), rb.get(f, "")
            t = classify(f, a, b)
            if t:
                out.append({"key": k, "field": f, "value_A": a, "value_B": b, "type": t})
    for n, d in enumerate(out, start=1):
        d["discrepancy_id"] = "D-%04d" % n
    return out, idx_a, idx_b, fields


def write_csv(path, columns, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})
    os.replace(tmp, path)


def cmd_diff(args):
    header_a, rows_a = read_csv(args.A, KEY_FIELDS, "A")
    header_b, rows_b = read_csv(args.B, KEY_FIELDS, "B")
    if header_a != header_b:
        warn("A and B headers differ; columns only in one file are compared as blank in the other (%s)"
             % ", ".join(sorted(set(header_a) ^ set(header_b))))
    disc, idx_a, idx_b, _ = compute_discrepancies(header_a, rows_a, header_b, rows_b)
    write_csv(args.out, DISCREPANCY_COLUMNS, disc)
    by_type = {}
    for d in disc:
        by_type[d["type"]] = by_type.get(d["type"], 0) + 1
    print("reconcile diff: %d rows in A, %d in B, %d keys in common, %d discrepancies -> %s" %
          (len(idx_a), len(idx_b), len(set(idx_a) & set(idx_b)), len(disc), args.out))
    for t in ["missing_in_A", "missing_in_B", "numeric", "text", "provenance"]:
        print("  %-13s %d" % (t, by_type.get(t, 0)))
    return 0


def validate_log(log_rows, disc):
    problems = []
    seen = {}
    disc_by_id = {d["discrepancy_id"]: d for d in disc}
    for i, r in enumerate(log_rows, start=2):
        did = r["discrepancy_id"]
        if did in seen:
            problems.append("adjudication log line %d: %s already adjudicated on line %d" % (i, did, seen[did]))
            continue
        seen[did] = i
        if did not in disc_by_id:
            problems.append("adjudication log line %d: %s is not a discrepancy of these two files (stale or wrong log)" % (i, did))
            continue
        d = disc_by_id[did]
        if r["decision"] not in ("A", "B", "other"):
            problems.append("adjudication log line %d (%s): decision must be A, B or other, got '%s'" % (i, did, r["decision"]))
        if r["decision"] == "other":
            if d["field"] == ROW_FIELD:
                problems.append("adjudication log line %d (%s): a whole-row discrepancy takes decision A or B, not other" % (i, did))
            elif r["chosen_value"] == "":
                problems.append("adjudication log line %d (%s): decision other needs a chosen_value" % (i, did))
        for f in ("adjudicator", "date", "reason"):
            if r[f] == "":
                problems.append("adjudication log line %d (%s): %s is blank" % (i, did, f))
        if r["date"]:
            try:
                _dt.date.fromisoformat(r["date"])
            except ValueError:
                problems.append("adjudication log line %d (%s): date '%s' is not ISO (YYYY-MM-DD)" % (i, did, r["date"]))
    unlogged = [d for d in disc if d["discrepancy_id"] not in seen]
    for d in unlogged:
        problems.append("discrepancy %s has no adjudication-log row (%s; field %s; A='%s'; B='%s'; type %s)" %
                        (d["discrepancy_id"], d["key"], d["field"], d["value_A"], d["value_B"], d["type"]))
    if unlogged:
        problems.append("refusing to build: %d of %d discrepancies are not adjudicated" % (len(unlogged), len(disc)))
    return problems, {r["discrepancy_id"]: r for r in log_rows}


def merge_meta(a, b, field):
    """Common value, or the only value (row kept from one file), or A=<a>;B=<b> when the two runs differ."""
    if a == b or b == "":
        return a
    if a == "":
        return b
    return "A=%s;B=%s" % (a, b)


def cmd_build(args):
    header_a, rows_a = read_csv(args.A, KEY_FIELDS, "A")
    header_b, rows_b = read_csv(args.B, KEY_FIELDS, "B")
    _, log_rows = read_csv(args.log, LOG_COLUMNS, "adjudication log")
    disc, idx_a, idx_b, fields = compute_discrepancies(header_a, rows_a, header_b, rows_b)
    problems, log = validate_log(log_rows, disc)
    primary = None
    if args.primary:
        _, prim_rows = read_csv(args.primary, PRIMARY_COLUMNS, "primary-outcome")
        primary = {}
        for i, r in enumerate(prim_rows, start=2):
            sa = (r["study_id"], r["ability_id"])
            if sa in primary and primary[sa] != r["outcome_measure"]:
                problems.append("primary-outcome file line %d: study %s x ability %s already has primary outcome '%s'; one per study x ability"
                                % (i, sa[0], sa[1], primary[sa]))
            primary[sa] = r["outcome_measure"]
    if problems:
        die(problems)

    out_cols = list(header_a) + [c for c in header_b if c not in header_a]
    if "is_primary_outcome" not in out_cols:
        out_cols.insert(out_cols.index("n_tested") + 1 if "n_tested" in out_cols else len(out_cols), "is_primary_outcome")
    disc_by_key = {}
    for d in disc:
        disc_by_key.setdefault(d["key"], []).append(d)
    build_date = args.date or _dt.date.today().isoformat()
    try:
        _dt.date.fromisoformat(build_date)
    except ValueError:
        die("--date '%s' is not ISO (YYYY-MM-DD)" % build_date)

    result = []
    dropped = 0
    for k in sorted(set(idx_a) | set(idx_b)):
        ra, rb = idx_a.get(k), idx_b.get(k)
        dlist = disc_by_key.get(k, [])
        row_d = [d for d in dlist if d["field"] == ROW_FIELD]
        if row_d:
            dec = log[row_d[0]["discrepancy_id"]]["decision"]
            src = ra if ra is not None else rb
            present_in = "A" if ra is not None else "B"
            if dec != present_in:  # adjudicator chose the file where the row is absent: drop it
                dropped += 1
                continue
            new = {c: src.get(c, "") for c in out_cols}
            meta_a = ra if ra is not None else {}
            meta_b = rb if rb is not None else {}
        else:
            new = {}
            for c in out_cols:
                if c in KEY_FIELDS or c in RUN_METADATA_FIELDS:
                    new[c] = ra.get(c, "") if c in KEY_FIELDS else ""
                else:
                    new[c] = ra.get(c, "") if ra.get(c, "") == rb.get(c, "") else None
            for d in dlist:
                entry = log[d["discrepancy_id"]]
                if entry["decision"] == "A":
                    new[d["field"]] = ra.get(d["field"], "")
                elif entry["decision"] == "B":
                    new[d["field"]] = rb.get(d["field"], "")
                else:
                    new[d["field"]] = entry["chosen_value"]
            for c in out_cols:
                if new[c] is None:  # equivalent but not identical numerics (e.g. 1 vs 1.0): keep A's printed form
                    new[c] = ra.get(c, "")
            meta_a, meta_b = ra, rb
        new["extractor_id"] = "reconciled"
        new["extraction_date"] = build_date
        new["skill_version"] = merge_meta(meta_a.get("skill_version", ""), meta_b.get("skill_version", ""), "skill_version")
        new["model"] = merge_meta(meta_a.get("model", ""), meta_b.get("model", ""), "model")
        result.append(new)

    # is_primary_outcome
    if primary is None:
        for r in result:
            r["is_primary_outcome"] = ""
        warn("no --primary file given: is_primary_outcome left blank on every row; analysis/00_load.R will refuse the file until it is set")
    else:
        matched = set()
        for r in result:
            sa = (r["study_id"], r["ability_id"])
            if sa in primary and primary[sa] == r["outcome_measure"]:
                r["is_primary_outcome"] = "yes"
                matched.add(sa)
            else:
                r["is_primary_outcome"] = "no"
        for sa in sorted({(r["study_id"], r["ability_id"]) for r in result} - matched):
            warn("study %s x ability %s has no is_primary_outcome = yes row (no matching primary-outcome entry)" % sa)
        for sa in sorted(set(primary) - matched):
            warn("primary-outcome entry %s x %s ('%s') matches no reconciled row" % (sa[0], sa[1], primary[sa]))

    write_csv(args.out, out_cols, result)
    print("reconcile build: %d discrepancies applied from %s; %d row(s) written, %d row(s) dropped by adjudication -> %s" %
          (len(disc), args.log, len(result), dropped, args.out))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Diff two extractor files and build the reconciled master (tools/RECONCILIATION.md)")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diff", help="list every field-level discrepancy between A and B")
    d.add_argument("A"); d.add_argument("B"); d.add_argument("--out", required=True)
    d.set_defaults(func=cmd_diff)
    b = sub.add_parser("build", help="apply the adjudication log and write master_reconciled.csv")
    b.add_argument("A"); b.add_argument("B"); b.add_argument("log"); b.add_argument("--out", required=True)
    b.add_argument("--primary", help="CSV with study_id, ability_id, outcome_measure naming the primary outcome per study x ability")
    b.add_argument("--date", help="extraction_date written on reconciled rows (default: today, ISO)")
    b.set_defaults(func=cmd_build)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
