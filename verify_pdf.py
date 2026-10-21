#!/usr/bin/env python3
"""Verify a generated CV/cover-letter PDF: page count, clean text layer, required text.

Uses PyMuPDF (fitz) directly rather than poppler's pdftotext/pdfinfo CLIs,
since those aren't reliably available in this environment.
"""

import argparse
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF


def normalize_text(text):
    return " ".join(text.split())


def verify_pdf(pdf_path, expected_pages=1, min_chars=50, required_text=()):
    """Return a list of issue strings. Empty list means the PDF passed."""
    pdf_path = Path(pdf_path)
    issues = []

    if not pdf_path.is_file():
        return [f"PDF does not exist: {pdf_path}"]

    doc = fitz.open(pdf_path)
    try:
        if expected_pages is not None and doc.page_count != expected_pages:
            issues.append(f"expected {expected_pages} page(s), found {doc.page_count}")

        raw_text = doc[0].get_text("text") if doc.page_count else ""
        text = normalize_text(raw_text)

        if len(text) < min_chars:
            issues.append(f"text layer has {len(text)} character(s); expected at least {min_chars}")

        if "�" in raw_text:
            issues.append("text layer contains replacement characters (\\ufffd) - likely a font/encoding issue")

        if re.search(r"\(cid:\d+\)", raw_text):
            issues.append("text layer contains raw (cid:*) markers - glyphs did not map to extractable text")

        for required in required_text:
            if normalize_text(required).lower() not in text.lower():
                issues.append(f"text layer is missing required text: {required!r}")
    finally:
        doc.close()

    return issues


def build_parser():
    parser = argparse.ArgumentParser(
        description="Verify a CV/cover-letter PDF's page count and ATS-readable text layer."
    )
    parser.add_argument("pdf", type=Path, help="PDF file to verify")
    parser.add_argument("--pages", type=int, default=1, help="required exact page count (default: 1)")
    parser.add_argument(
        "--min-chars",
        type=int,
        default=50,
        help="minimum non-whitespace text-layer characters (default: 50)",
    )
    parser.add_argument(
        "--contains",
        action="append",
        default=[],
        help="text that must appear after whitespace normalization; repeatable "
        "(e.g. --contains \"Jane Doe\" --contains jane.doe@example.com)",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    issues = verify_pdf(args.pdf, args.pages, args.min_chars, args.contains)
    if issues:
        print(f"FAILED: {args.pdf}", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    print(f"Verified: {args.pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
