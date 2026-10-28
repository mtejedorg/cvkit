#!/usr/bin/env python3
"""Fail if any tracked (or untracked, non-ignored) file contains a personal-data pattern.

Patterns come from <workspace>/_private/privacy_patterns.txt (one literal per line,
"#" comments allowed). Run it before every commit and before publishing a site:

    python privacy_check.py                       # scan the repository
    python privacy_check.py --paths site/ docs/   # scan specific paths
    python privacy_check.py --patterns other.txt --paths ../portfolio_site
    python privacy_check.py --history             # every commit reachable from HEAD: diffs, messages, author/committer
    python privacy_check.py --history --all-refs  # every branch and tag too

Exit code 1 on any hit. Without a patterns file it warns and exits 0 so that
other users of the skill are not blocked.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from cvtool.privacy import load_patterns, scan_history, scan_paths
from cvtool.workspace import repo_root, resolve_workspace


def git_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, check=True, capture_output=True,
    ).stdout
    return [root / p for p in out.decode("utf-8", "ignore").split("\0") if p]


def expand(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(q for q in p.rglob("*") if q.is_file() and ".git" not in q.parts)
        elif p.is_file():
            files.append(p)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--patterns", type=Path, default=None, help="patterns file (default: <workspace>/_private/privacy_patterns.txt)")
    parser.add_argument("--paths", nargs="*", default=None, help="files or folders to scan (default: git files of this repo)")
    parser.add_argument("--history", action="store_true", help="scan every commit reachable from HEAD (diffs, messages, author and committer) instead of the working files")
    parser.add_argument("--all-refs", action="store_true", help="with --history: every local and remote branch and tag, not only HEAD")
    args = parser.parse_args(argv)

    root = repo_root()
    ws = resolve_workspace(root)
    patterns_path = args.patterns or (ws.private_dir / "privacy_patterns.txt")
    patterns = load_patterns(patterns_path)
    if not patterns:
        print(f"privacy_check: WARNING no patterns file at {patterns_path}; nothing was checked.", file=sys.stderr)
        return 0

    if args.history:
        history_hits, addresses = scan_history(root, patterns, all_refs=args.all_refs)
        print("privacy_check: commit identities: " + (", ".join(addresses) or "none"))
        if history_hits:
            print(f"privacy_check: {len(history_hits)} history hit(s) for {len(patterns)} pattern(s):", file=sys.stderr)
            for hit in history_hits:
                print(f"  {hit.commit} ({hit.where}): {hit.pattern}", file=sys.stderr)
            return 1
        print(f"privacy_check: history clean against {len(patterns)} pattern(s).")
        return 0

    files = expand(args.paths) if args.paths else git_files(root)
    files = [f for f in files if f.resolve() != patterns_path.resolve()]
    hits = scan_paths(files, patterns)
    if hits:
        print(f"privacy_check: {len(hits)} hit(s) for {len(patterns)} pattern(s):", file=sys.stderr)
        for hit in hits:
            print(f"  {hit.path}:{hit.line}: {hit.pattern}", file=sys.stderr)
        return 1
    print(f"privacy_check: {len(files)} file(s) clean against {len(patterns)} pattern(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
