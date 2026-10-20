import contextlib
import datetime
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import tracker  # noqa: E402


class NormalizeUrlTests(unittest.TestCase):
    def test_same_posting_different_links(self):
        a = tracker.normalize_url("https://www.bayt.com/en/kuwait/jobs/it-support-123/?utm_source=x&b=2&a=1#top")
        b = tracker.normalize_url("bayt.com/en/kuwait/jobs/it-support-123?a=1&b=2")
        self.assertEqual(a, b)

    def test_different_postings_stay_different(self):
        self.assertNotEqual(tracker.normalize_url("https://bayt.com/jobs/1"),
                            tracker.normalize_url("https://bayt.com/jobs/2"))

    def test_empty(self):
        self.assertEqual(tracker.normalize_url(""), "")


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "sub", "tracker.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_save_reload(self):
        t = tracker.Tracker(self.path)
        row, created = t.add("Zain", "IT Support Engineer", "https://bayt.com/jobs/1", source="bayt", fit=80)
        self.assertTrue(created)
        self.assertEqual(row["id"], "1")
        t.save()
        again = tracker.Tracker(self.path)
        self.assertEqual(len(again.rows), 1)
        self.assertEqual(again.rows[0]["company"], "Zain")
        self.assertEqual(again.rows[0]["fit"], "80")

    def test_duplicate_url_is_not_added_twice(self):
        t = tracker.Tracker(self.path)
        t.add("NBK", "Network Engineer", "https://www.linkedin.com/jobs/view/42/?trk=abc")
        row, created = t.add("NBK", "Network Engineer", "https://linkedin.com/jobs/view/42")
        self.assertFalse(created)
        self.assertEqual(len(t.rows), 1)
        self.assertEqual(row["id"], "1")

    def test_ids_increase(self):
        t = tracker.Tracker(self.path)
        t.add("A", "r1", "https://x.com/1")
        row, _ = t.add("B", "r2", "https://x.com/2")
        self.assertEqual(row["id"], "2")

    def test_update_status_and_note(self):
        t = tracker.Tracker(self.path)
        t.add("KOC", "Engineer", "https://koc.com.kw/jobs/7")
        row = t.update("1", status="applied", note="Sent via careers site")
        self.assertEqual(row["status"], "applied")
        self.assertIn("Sent via careers site", row["notes"])

    def test_bad_status_and_fit_are_rejected(self):
        t = tracker.Tracker(self.path)
        with self.assertRaises(ValueError):
            t.add("A", "r", status="maybe")
        with self.assertRaises(ValueError):
            t.add("A", "r", fit=150)
        with self.assertRaises(KeyError):
            t.update("99", status="applied")

    def test_formula_cells_are_neutralised(self):
        t = tracker.Tracker(self.path)
        row, _ = t.add("=HYPERLINK(\"evil\")", "@role", "https://x.com/9", note="+cmd")
        self.assertTrue(row["company"].startswith("'="))
        self.assertTrue(row["role"].startswith("'@"))
        self.assertTrue(row["notes"].startswith("'+"))

    def test_followups(self):
        t = tracker.Tracker(self.path)
        t.add("A", "r", "https://x.com/1", status="applied")
        t.add("B", "r", "https://x.com/2", status="found")
        t.rows[0]["updated"] = "2026-01-01"
        t.rows[1]["updated"] = "2026-01-01"
        due = t.followups(days=10, on=datetime.date(2026, 1, 20))
        self.assertEqual([row["company"] for row in due], ["A"])
        self.assertEqual(t.followups(days=30, on=datetime.date(2026, 1, 20)), [])

    def test_stats(self):
        t = tracker.Tracker(self.path)
        t.add("A", "r", "https://x.com/1", status="applied")
        t.add("B", "r", "https://x.com/2", status="applied")
        t.add("C", "r", "https://x.com/3", status="rejected")
        counts = t.stats()
        self.assertEqual(counts["applied"], 2)
        self.assertEqual(counts["rejected"], 1)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "tracker.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = tracker.main(["--file", self.path] + list(args))
        return code, out.getvalue()

    def test_add_seen_update_list(self):
        code, out = self.run_cli("add", "--company", "Boubyan Bank", "--role", "IT Support",
                                 "--url", "https://gulftalent.com/kuwait/jobs/5", "--fit", "72")
        self.assertEqual(code, 0)
        self.assertIn("Added #1", out)
        self.assertEqual(self.run_cli("seen", "https://www.gulftalent.com/kuwait/jobs/5/")[0], 0)
        self.assertEqual(self.run_cli("seen", "https://gulftalent.com/kuwait/jobs/6")[0], 1)
        self.assertEqual(self.run_cli("update", "1", "--status", "applied")[0], 0)
        code, out = self.run_cli("list", "--status", "applied")
        self.assertIn("Boubyan Bank", out)

    def test_update_unknown_id_fails_cleanly(self):
        self.assertEqual(self.run_cli("update", "7", "--status", "applied")[0], 2)

    def test_empty_list(self):
        code, out = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("No applications yet", out)


if __name__ == "__main__":
    unittest.main()
