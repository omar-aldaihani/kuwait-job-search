#!/usr/bin/env python3
"""Turn an HTML CV or cover letter into a PDF using Edge or Chrome.

Microsoft Edge ships with every Windows 10/11 PC, so nothing extra has to be
installed (no LaTeX, no Word). Chrome or Chromium also work.

    python tools/render_pdf.py applications/zain_it-support/cv.html
    python tools/render_pdf.py cover.html --out cover.pdf --expect-pages 1

Prints the PDF path and its page count. With --expect-pages, exits with code 3
when the page count is different, so Claude knows to shorten the document.
"""

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CANDIDATES = {
    "nt": [
        r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        r"%LocalAppData%\Google\Chrome\Application\chrome.exe",
    ],
    "darwin": [
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
    "posix": ["microsoft-edge", "google-chrome", "google-chrome-stable", "chromium",
              "chromium-browser", "chrome"],
}


def find_browser(env=None):
    """Return the path of an installed Edge/Chrome, or None."""
    env = env if env is not None else os.environ
    override = env.get("KJS_BROWSER")
    if override and os.path.exists(override):
        return override
    if os.name == "nt":
        for raw in CANDIDATES["nt"]:
            path = os.path.expandvars(raw)
            if os.path.exists(path):
                return path
        return None
    if sys.platform == "darwin":
        for path in CANDIDATES["darwin"]:
            if os.path.exists(path):
                return path
    for name in CANDIDATES["posix"]:
        found = shutil.which(name)
        if found:
            return found
    return None


def count_pages(pdf_path):
    """Count pages in a PDF without any extra library.

    Good enough for the PDFs a Chromium browser writes (uncompressed page tree).
    """
    data = pathlib.Path(pdf_path).read_bytes()
    counts = [int(n) for n in re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", data)]
    counts += [int(n) for n in re.findall(rb"/Count\s+(\d+)[^>]*?/Type\s*/Pages\b", data)]
    if counts:
        return max(counts)
    return len(re.findall(rb"/Type\s*/Page\b(?!s)", data))


def render(html_path, pdf_path=None, browser=None, timeout=60):
    html = pathlib.Path(html_path).resolve()
    if not html.exists():
        raise FileNotFoundError("No such file: %s" % html)
    pdf = pathlib.Path(pdf_path).resolve() if pdf_path else html.with_suffix(".pdf")
    browser = browser or find_browser()
    if not browser:
        raise RuntimeError("Could not find Microsoft Edge or Google Chrome. Install one, or set "
                           "KJS_BROWSER to the browser's full path.")
    with tempfile.TemporaryDirectory() as profile:
        cmd = [browser, "--headless", "--disable-gpu", "--no-sandbox",
               "--no-first-run", "--user-data-dir=%s" % profile,
               "--no-pdf-header-footer", "--print-to-pdf-no-header",
               "--print-to-pdf=%s" % pdf, html.as_uri()]
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if not pdf.exists() or pdf.stat().st_size == 0:
        raise RuntimeError("The browser did not write a PDF.\n%s" % (done.stderr or done.stdout)[-800:])
    return pdf


def main(argv=None):
    parser = argparse.ArgumentParser(prog="render_pdf", description="HTML to PDF with Edge/Chrome.")
    parser.add_argument("html")
    parser.add_argument("--out", help="PDF path (default: same name as the HTML)")
    parser.add_argument("--expect-pages", type=int, help="fail (exit 3) if the page count differs")
    args = parser.parse_args(argv)
    try:
        pdf = render(args.html, args.out)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print("Error: %s" % exc, file=sys.stderr)
        return 2
    pages = count_pages(pdf)
    print("%s (%d page%s)" % (pdf, pages, "" if pages == 1 else "s"))
    if args.expect_pages and pages != args.expect_pages:
        print("Expected %d page(s) but got %d. Shorten or tighten the document."
              % (args.expect_pages, pages), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
