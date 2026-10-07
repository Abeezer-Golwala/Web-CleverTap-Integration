#!/usr/bin/env python3
"""Check profiles whose `identity` field holds more than one id.

For every row the identity value is split on commas and each id is classified
as an email (contains "@") or an other id. Emails containing uppercase letters
are ignored. Two new columns are written so the values can be checked easily:

    emails     - the (lowercase) emails, joined with ", "
    other_ids  - every non-email id, joined with ", "

Usage:
    python3 check_identities.py input.csv [output.csv]
"""
import csv
import sys


def split_identity(value):
    ids = [i.strip() for i in (value or "").split(",") if i.strip()]
    emails, others = [], []
    for i in ids:
        if "@" in i:
            if i != i.lower():  # ignore capital email ids
                continue
            emails.append(i)
        else:
            others.append(i)
    return ids, emails, others


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else "identity_check_output.csv"

    with open(src, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    total = len(rows)
    multi_id = multi_email = 0
    out_rows = []
    for row in rows:
        ids, emails, others = split_identity(row.get("identity", ""))
        if len(ids) > 1:
            multi_id += 1
        if len(emails) > 1:
            multi_email += 1
        row["emails"] = ", ".join(emails)
        row["other_ids"] = ", ".join(others)
        row["email_count"] = len(emails)
        out_rows.append(row)

    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields + ["emails", "other_ids", "email_count"])
        w.writeheader()
        w.writerows(out_rows)

    print(f"Total profiles:                           {total}")
    print(f"Profiles with more than 1 id:             {multi_id}")
    print(f"Profiles with more than 1 email (lowercase only): {multi_email}")
    print(f"Output written to: {dst}")


if __name__ == "__main__":
    main()
