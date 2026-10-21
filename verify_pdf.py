#!/usr/bin/env python3
"""Verify a generated PDF: page count, clean text layer, required/forbidden text, section order.

Example (CV):
    python verify_pdf.py "_generated/Acme/CV_Jane_Doe.pdf" --max-pages 2 \
        --contains "Jane Doe" --contains jane.doe@example.com \
        --order "Professional Summary" --order "Professional Experience" --order "Education"

Example (public variant, phone must be absent):
    python verify_pdf.py "_generated/Generic/CV_Jane_Doe_public.pdf" --max-pages 2 --forbids "555 010"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cvtool.verify import verify_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", type=Path, help="PDF file to verify")
    parser.add_argument("--pages", type=int, default=None, help="required exact page count")
    parser.add_argument("--max-pages", type=int, default=None, help="maximum page count")
    parser.add_argument("--min-chars", type=int, default=50, help="minimum text-layer characters (default: 50)")
    parser.add_argument("--contains", action="append", default=[], help="text that must appear (repeatable)")
    parser.add_argument("--forbids", action="append", default=[], help="text that must NOT appear (repeatable)")
    parser.add_argument("--order", action="append", default=[], help="texts that must appear in this order (repeatable)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issues = verify_pdf(
        args.pdf,
        pages=args.pages,
        max_pages=args.max_pages,
        min_chars=args.min_chars,
        required_text=args.contains,
        forbidden_text=args.forbids,
        order=args.order,
    )
    if issues:
        print(f"FAILED: {args.pdf}", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    print(f"Verified: {args.pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
