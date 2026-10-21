"""Check a compiled PDF the way an applicant tracking system would read it."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

import fitz  # PyMuPDF


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def verify_pdf(
    pdf_path: Path,
    *,
    pages: int | None = None,
    max_pages: int | None = None,
    min_chars: int = 50,
    required_text: Sequence[str] = (),
    forbidden_text: Sequence[str] = (),
    order: Sequence[str] = (),
) -> list[str]:
    """Return a list of issues. An empty list means the PDF passed."""
    pdf_path = Path(pdf_path)
    if not pdf_path.is_file():
        return [f"PDF does not exist: {pdf_path}"]

    issues: list[str] = []
    doc = fitz.open(pdf_path)
    try:
        if pages is not None and doc.page_count != pages:
            issues.append(f"expected {pages} page(s), found {doc.page_count}")
        if max_pages is not None and doc.page_count > max_pages:
            issues.append(f"exceeds max pages: {doc.page_count} > {max_pages}")

        raw_text = "\n".join(page.get_text("text") for page in doc)
    finally:
        doc.close()

    text = normalize_text(raw_text)
    lowered = text.lower()

    if len(text) < min_chars:
        issues.append(f"text layer has {len(text)} character(s); expected at least {min_chars}")
    if "�" in raw_text:
        issues.append("text layer contains replacement characters (\\ufffd), likely a font/encoding issue")
    if re.search(r"\(cid:\d+\)", raw_text):
        issues.append("text layer contains raw (cid:*) markers; glyphs did not map to extractable text")

    for required in required_text:
        if normalize_text(required).lower() not in lowered:
            issues.append(f"text layer is missing required text: {required!r}")
    for forbidden in forbidden_text:
        if normalize_text(forbidden).lower() in lowered:
            issues.append(f"text layer contains forbidden text: {forbidden!r}")

    positions: list[tuple[str, int]] = []
    for heading in order:
        idx = lowered.find(normalize_text(heading).lower())
        if idx < 0:
            issues.append(f"order check: text not found: {heading!r}")
        else:
            positions.append((heading, idx))
    for (a, ia), (b, ib) in zip(positions, positions[1:]):
        if ib < ia:
            issues.append(f"order violated: {b!r} appears before {a!r}")

    return issues
