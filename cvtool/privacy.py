"""Scan files for personal-data patterns before anything is committed or published.

Patterns are literal strings, one per line, case-insensitive. A pattern that is a
single word (letters only) must match as a whole word; anything else (emails,
phone fragments, phrases) matches as a substring.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

RECORD = chr(0x1e)  # separators written by the git log formats below
FIELD = chr(0x1f)
NL = chr(10)

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


@dataclass(frozen=True)
class HistoryHit:
    commit: str
    where: str  # "metadata" (author, committer, message) or "diff"
    pattern: str


def _git_log(repo: Path, rev: str, fmt: str, *extra: str) -> str:
    out = subprocess.run(
        ["git", "log", rev, f"--format={fmt}", *extra],
        cwd=repo, check=True, capture_output=True,
    ).stdout
    return out.decode("utf-8", "ignore")


def scan_history(repo: Path, patterns: Sequence[str], all_refs: bool = False) -> tuple[list[HistoryHit], list[str]]:
    """Scan every commit reachable from HEAD (all refs with `all_refs`): author and committer, message, and each diff.

    A pattern that was ever committed shows up in some diff, so this also finds
    content that a later commit removed. Returns the hits and the distinct
    author/committer addresses, so the caller can confirm the identity by eye.
    """
    repo = Path(repo)
    hits: list[HistoryHit] = []
    addresses: set[str] = set()

    rev = "--all" if all_refs else "HEAD"
    meta = _git_log(repo, rev, "%x1e%H%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B")
    for record in meta.split(RECORD):
        if not record.strip():
            continue
        sha, *fields = record.split(FIELD)
        sha = sha.strip()
        addresses.update(f.strip() for f in fields[1:4:2] if f.strip())
        for pattern in sorted({p for p, _ in scan_text(NL.join(fields), patterns)}):
            hits.append(HistoryHit(sha[:10], "metadata", pattern))

    patches = _git_log(repo, rev, "%x1e%H", "-p", "-U0", "-m", "--no-color")
    for record in patches.split(RECORD):
        if not record.strip():
            continue
        sha, _, body = record.partition(NL)
        for pattern in sorted({p for p, _ in scan_text(body, patterns)}):
            hits.append(HistoryHit(sha.strip()[:10], "diff", pattern))
    return hits, sorted(addresses)
