#!/usr/bin/env python3
"""Compile the Markdown files of one application folder (or all) to A4 PDFs.

Usage:
    python compile_all_pdfs.py "<FolderName>" [--force] [--public]
    python compile_all_pdfs.py                  # every folder, only stale PDFs

Folders live in <workspace>/_generated/. The workspace is resolved from
CV_WORKSPACE, cv-builder.config.json, or this repository (see cvtool/workspace.py).
--public writes <name>_public.pdf with every <span class="private"> removed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cvtool.compile import compile_folder, find_edge
from cvtool.workspace import repo_root, resolve_workspace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", nargs="?", help='application folder name, e.g. "Acme_Corp" (or _generated/Acme_Corp)')
    parser.add_argument("--force", action="store_true", help="recompile even if the PDF is newer than the Markdown")
    parser.add_argument("--public", action="store_true", help="write *_public.pdf without private spans (phone)")
    args = parser.parse_args(argv)

    ws = resolve_workspace(repo_root())
    generated = ws.generated_dir
    if not generated.is_dir():
        print(f"Output folder not found: {generated}. Create _generated/<FolderName>/ with your Markdown files first.", file=sys.stderr)
        return 1

    edge = find_edge()
    if args.folder:
        name = Path(args.folder.rstrip("/\\")).name
        folders = [generated / name]
        if not folders[0].is_dir():
            print(f"No such folder: {folders[0]}", file=sys.stderr)
            return 1
        force = True if not args.force else args.force
    else:
        folders = [p for p in sorted(generated.iterdir()) if p.is_dir()]
        force = args.force

    total = 0
    for folder in folders:
        try:
            total += len(compile_folder(folder, force=force, public=args.public, edge_path=edge))
        except Exception as exc:  # keep going with the other folders
            print(f"Error compiling {folder}: {exc}", file=sys.stderr)
    print(f"{total} PDF(s) written (workspace: {ws.root}, via {ws.source}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
