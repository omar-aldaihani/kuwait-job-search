import os
import pathlib
import re
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import render_pdf  # noqa: E402

TEMPLATES = ["cv.html", "cover_letter.html", "cover_letter_ar.html"]


class PageCountTests(unittest.TestCase):
    def write(self, data):
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        handle.write(data)
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    def test_count_from_page_tree(self):
        pdf = self.write(b"%PDF-1.4\n1 0 obj << /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >> endobj\n"
                         b"3 0 obj << /Type /Page >> endobj 4 0 obj << /Type /Page >> endobj")
        self.assertEqual(render_pdf.count_pages(pdf), 2)

    def test_count_with_count_before_type(self):
        pdf = self.write(b"%PDF-1.4\n1 0 obj << /Count 1 /Kids [3 0 R] /Type /Pages >> endobj")
        self.assertEqual(render_pdf.count_pages(pdf), 1)

    def test_fallback_counts_page_objects(self):
        pdf = self.write(b"%PDF-1.4 << /Type /Page >> << /Type /Page >> << /Type /Page >>")
        self.assertEqual(render_pdf.count_pages(pdf), 3)


class BrowserTests(unittest.TestCase):
    def test_override_is_used(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        self.addCleanup(os.unlink, path)
        self.assertEqual(render_pdf.find_browser({"KJS_BROWSER": path}), path)

    def test_missing_html_raises(self):
        with self.assertRaises(FileNotFoundError):
            render_pdf.render("does-not-exist.html", browser="x")


class TemplateTests(unittest.TestCase):
    def test_templates_have_placeholders_and_a4(self):
        for name in TEMPLATES:
            text = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn("size: A4", text, name)
            self.assertRegex(text, r"\{\{[A-Z_]+", name)

    def test_arabic_template_is_rtl(self):
        text = (ROOT / "templates" / "cover_letter_ar.html").read_text(encoding="utf-8")
        self.assertIn('dir="rtl"', text)

    @unittest.skipUnless(render_pdf.find_browser(), "no Edge/Chrome installed")
    def test_real_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = pathlib.Path(tmp) / "cv.html"
            text = (ROOT / "templates" / "cv.html").read_text(encoding="utf-8")
            html.write_text(re.sub(r"\{\{[^}]*\}\}", "Sample", text), encoding="utf-8")
            pdf = render_pdf.render(html)
            self.assertEqual(render_pdf.count_pages(pdf), 1)


if __name__ == "__main__":
    unittest.main()
