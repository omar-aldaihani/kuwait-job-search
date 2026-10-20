#!/usr/bin/env python3
"""Application tracker for kuwait-job-search (standard library only).

Keeps every job you look at in one CSV file (applications/tracker.csv by default)
so Claude never shows you the same posting twice and you can see what needs a
follow-up.

    python tools/tracker.py add --company "Zain" --role "IT Support Engineer" --url URL --source bayt --fit 78
    python tools/tracker.py list
    python tools/tracker.py list --status applied
    python tools/tracker.py update 3 --status interview --note "Phone screen Sunday 10am"
    python tools/tracker.py seen URL          # exit code 0 if already tracked, 1 if new
    python tools/tracker.py followups --days 10
    python tools/tracker.py stats
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
import urllib.parse

DEFAULT_PATH = os.path.join("applications", "tracker.csv")

FIELDS = ["id", "added", "updated", "company", "role", "location", "source", "url",
          "fit", "status", "deadline", "notes"]

# The order an application normally moves through.
STATUSES = ["found", "shortlisted", "applied", "interview", "offer", "accepted",
            "rejected", "withdrawn", "skipped"]
OPEN_STATUSES = {"applied", "interview"}

# Query parameters that only track where a click came from.
_TRACKING = re.compile(r"^(utm_|fbclid|gclid|trk|ref|refid|src|source|from)", re.I)


def today():
    return datetime.date.today().isoformat()


def normalize_url(url):
    """Make two links to the same posting compare equal.

    Lower-cases the host, drops 'www.', tracking parameters, fragments and a
    trailing slash, and sorts the remaining query parameters.
    """
    if not url:
        return ""
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
             if not _TRACKING.match(k)]
    query.sort()
    path = parts.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit(("https", host, path, urllib.parse.urlencode(query), ""))


def _clean_cell(value):
    """Stop spreadsheet apps from running a cell as a formula (CSV injection)."""
    text = "" if value is None else str(value)
    text = text.replace("\r", " ").replace("\n", " ").strip()
    if text[:1] in ("=", "+", "-", "@", "\t"):
        text = "'" + text
    return text


class Tracker:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.rows = []
        if os.path.exists(path):
            with open(path, newline="", encoding="utf-8") as handle:
                self.rows = [dict(row) for row in csv.DictReader(handle)]

    def save(self):
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            for row in self.rows:
                writer.writerow({key: row.get(key, "") for key in FIELDS})
        os.replace(tmp, self.path)

    def next_id(self):
        ids = [int(row["id"]) for row in self.rows if str(row.get("id", "")).isdigit()]
        return str(max(ids) + 1 if ids else 1)

    def find_url(self, url):
        key = normalize_url(url)
        if not key:
            return None
        for row in self.rows:
            if normalize_url(row.get("url", "")) == key:
                return row
        return None

    def get(self, row_id):
        for row in self.rows:
            if row.get("id") == str(row_id):
                return row
        return None

    def add(self, company, role, url="", location="Kuwait", source="", fit="",
            status="found", deadline="", note=""):
        if status not in STATUSES:
            raise ValueError("Unknown status %r. Use one of: %s" % (status, ", ".join(STATUSES)))
        if fit not in ("", None):
            fit = int(fit)
            if not 0 <= fit <= 100:
                raise ValueError("Fit must be between 0 and 100.")
        existing = self.find_url(url) if url else None
        if existing:
            return existing, False
        row = {
            "id": self.next_id(), "added": today(), "updated": today(),
            "company": _clean_cell(company), "role": _clean_cell(role),
            "location": _clean_cell(location), "source": _clean_cell(source),
            "url": url.strip() if url else "", "fit": "" if fit in ("", None) else str(fit),
            "status": status, "deadline": _clean_cell(deadline), "notes": _clean_cell(note),
        }
        self.rows.append(row)
        return row, True

    def update(self, row_id, status=None, note=None, fit=None, deadline=None):
        row = self.get(row_id)
        if row is None:
            raise KeyError("No application with id %s." % row_id)
        if status:
            if status not in STATUSES:
                raise ValueError("Unknown status %r. Use one of: %s" % (status, ", ".join(STATUSES)))
            row["status"] = status
        if note:
            stamp = "%s: %s" % (today(), _clean_cell(note))
            row["notes"] = (row.get("notes", "") + " | " + stamp).strip(" |")
        if fit is not None:
            row["fit"] = str(int(fit))
        if deadline:
            row["deadline"] = _clean_cell(deadline)
        row["updated"] = today()
        return row

    def filtered(self, status=None):
        rows = self.rows
        if status:
            rows = [row for row in rows if row.get("status") == status]
        return rows

    def followups(self, days=10, on=None):
        """Open applications with no update for `days` days or more."""
        on = on or datetime.date.today()
        due = []
        for row in self.rows:
            if row.get("status") not in OPEN_STATUSES:
                continue
            try:
                updated = datetime.date.fromisoformat(row.get("updated", ""))
            except ValueError:
                continue
            if (on - updated).days >= days:
                due.append(row)
        return due

    def stats(self):
        counts = {status: 0 for status in STATUSES}
        for row in self.rows:
            counts[row.get("status", "found")] = counts.get(row.get("status", "found"), 0) + 1
        return counts


def _table(rows):
    if not rows:
        return "No applications yet."
    cols = [("id", 3), ("status", 11), ("fit", 3), ("company", 22), ("role", 34), ("updated", 10)]
    lines = ["  ".join(name.upper().ljust(width) for name, width in cols)]
    for row in rows:
        cells = []
        for name, width in cols:
            text = str(row.get(name, ""))
            cells.append((text[: width - 1] + "…") if len(text) > width else text.ljust(width))
        lines.append("  ".join(cells))
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(prog="tracker", description="Track Kuwait job applications.")
    parser.add_argument("--file", default=DEFAULT_PATH, help="tracker CSV (default: %(default)s)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="add a posting")
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--url", default="")
    p.add_argument("--location", default="Kuwait")
    p.add_argument("--source", default="", help="bayt, linkedin, gulftalent, company site...")
    p.add_argument("--fit", type=int, default=None, help="fit score 0-100")
    p.add_argument("--status", default="found", choices=STATUSES)
    p.add_argument("--deadline", default="")
    p.add_argument("--note", default="")

    p = sub.add_parser("update", help="change status or add a note")
    p.add_argument("id")
    p.add_argument("--status", choices=STATUSES)
    p.add_argument("--note")
    p.add_argument("--fit", type=int)
    p.add_argument("--deadline")

    p = sub.add_parser("list", help="show applications")
    p.add_argument("--status", choices=STATUSES)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("seen", help="exit 0 if the URL is already tracked, 1 if new")
    p.add_argument("url")

    p = sub.add_parser("followups", help="applications waiting too long for a reply")
    p.add_argument("--days", type=int, default=10)
    p.add_argument("--json", action="store_true")

    sub.add_parser("stats", help="count applications by status")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    tracker = Tracker(args.file)

    try:
        if args.cmd == "add":
            row, created = tracker.add(args.company, args.role, args.url, args.location,
                                       args.source, args.fit, args.status, args.deadline, args.note)
            if created:
                tracker.save()
                print("Added #%s: %s - %s" % (row["id"], row["company"], row["role"]))
            else:
                print("Already tracked as #%s (%s)." % (row["id"], row["status"]))
            return 0

        if args.cmd == "update":
            row = tracker.update(args.id, args.status, args.note, args.fit, args.deadline)
            tracker.save()
            print("Updated #%s: %s" % (row["id"], row["status"]))
            return 0
    except (ValueError, KeyError) as exc:
        print("Error: %s" % (exc.args[0] if exc.args else exc), file=sys.stderr)
        return 2

    if args.cmd == "list":
        rows = tracker.filtered(args.status)
        print(json.dumps(rows, indent=2, ensure_ascii=False) if args.json else _table(rows))
        return 0

    if args.cmd == "seen":
        row = tracker.find_url(args.url)
        if row:
            print("Seen: #%s %s - %s (%s)" % (row["id"], row["company"], row["role"], row["status"]))
            return 0
        print("New")
        return 1

    if args.cmd == "followups":
        rows = tracker.followups(args.days)
        print(json.dumps(rows, indent=2, ensure_ascii=False) if args.json else _table(rows))
        return 0

    if args.cmd == "stats":
        for status, count in tracker.stats().items():
            if count:
                print("%-12s %d" % (status, count))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
