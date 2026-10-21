"""Scan files for personal-data patterns before anything is committed or published.

Patterns are literal strings, one per line, case-insensitive. A pattern that is a
single word (letters only) must match as a whole word; anything else (emails,
phone fragments, phrases) matches as a substring.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

_WORD = re.compile(r"[A-Za-zÀ-ɏ]+")


@dataclass(frozen=True)
class Hit:
    path: Path
    line: int
    pattern: str


def load_patterns(path: Path) -> list[str]:
    path = Path(path)
    if not path.is_file():
        return []
    patterns = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def _compile(pattern: str) -> re.Pattern[str]:
    if _WORD.fullmatch(pattern):
        return re.compile(rf"\b{re.escape(pattern)}\b", re.IGNORECASE)
    return re.compile(re.escape(pattern), re.IGNORECASE)


def scan_text(text: str, patterns: Sequence[str]) -> list[tuple[str, int]]:
    compiled = [(p, _compile(p)) for p in patterns]
    hits: list[tuple[str, int]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern, rx in compiled:
            if rx.search(line):
                hits.append((pattern, lineno))
    return hits


def is_binary(path: Path) -> bool:
    try:
        with open(path, "rb") as fh:
            return b"\x00" in fh.read(8192)
    except OSError:
        return True


def scan_paths(paths: Sequence[Path], patterns: Sequence[str]) -> list[Hit]:
    hits: list[Hit] = []
    for path in paths:
        path = Path(path)
        if not path.is_file() or is_binary(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern, line in scan_text(text, patterns):
            hits.append(Hit(path, line, pattern))
    return hits
