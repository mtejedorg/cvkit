#!/usr/bin/env python3
"""Deterministic helpers for the portfolio skill. Standard library only; Pillow for `preview`.

  detect   [path]                  -> hub | project | none
  remote   [path]                  -> owner, repo, hub and project URLs from the git remote
  validate <manifest.json>         -> contract errors (exit 1 if any)
  discover [--local-root DIR] [--owner O] [--hidden a,b] [--projects a,b]
                                   -> every manifest found locally or via gh + Pages, as JSON
  preview  <src> <dst>             -> 1200x675 JPEG under 300 KB
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = 1
STATUSES = {"in development", "released", "prototype", "archived"}
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED = ["schema", "name", "slug", "status", "blurb", "tags", "preview", "site", "repo", "pages", "updated"]
OPTIONAL = {"engine", "base_url"}
MANIFEST_PATHS = ("docs/site/portfolio.json", "site/portfolio.json")
HUB_CONFIG_PATHS = ("portfolio.hub.json", "portfolio_site/portfolio.hub.json", "site/portfolio.hub.json")
MAX_BLURB_WORDS = 45
MAX_TAGS = 5


# --- git remote ------------------------------------------------------------

@dataclass(frozen=True)
class Remote:
    owner: str
    repo: str

    @property
    def hub_url(self) -> str:
        return f"https://{self.owner.lower()}.github.io/"

    @property
    def project_url(self) -> str:
        return f"https://{self.owner.lower()}.github.io/{self.repo}/"

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"


def parse_remote(url: str) -> Remote | None:
    """Accept git@github.com:owner/repo.git, https://github.com/owner/repo(.git), ssh://git@github.com/owner/repo."""
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$", url.strip())
    if not m:
        return None
    return Remote(m.group("owner"), m.group("repo"))


def git_remote(path: Path) -> Remote | None:
    try:
        out = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return parse_remote(out)


# --- role detection --------------------------------------------------------

def detect_role(path: Path) -> str:
    path = Path(path)
    if any((path / p).is_file() for p in HUB_CONFIG_PATHS):
        return "hub"
    if any((path / p).is_file() for p in MANIFEST_PATHS):
        return "project"
    return "none"


def find_manifest(path: Path) -> Path | None:
    for p in MANIFEST_PATHS:
        if (Path(path) / p).is_file():
            return Path(path) / p
    return None


# --- validation ------------------------------------------------------------

def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not a JSON object"]
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing key: {key}")
    for key in data:
        if key not in REQUIRED and key not in OPTIONAL:
            errors.append(f"unknown key: {key}")
    if errors:
        return errors
    if data["schema"] != SCHEMA_VERSION:
        errors.append(f"schema must be {SCHEMA_VERSION}, got {data['schema']!r}")
    if not isinstance(data["name"], str) or not 1 <= len(data["name"]) <= 80:
        errors.append("name must be a string of 1-80 characters")
    if not isinstance(data["slug"], str) or not SLUG_RE.match(data["slug"]):
        errors.append("slug must be lowercase letters, digits and hyphens, starting with a letter")
    if data["status"] not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")
    if not isinstance(data["blurb"], str) or not data["blurb"].strip():
        errors.append("blurb must be a non-empty string")
    elif len(data["blurb"].split()) > MAX_BLURB_WORDS:
        errors.append(f"blurb has {len(data['blurb'].split())} words; at most {MAX_BLURB_WORDS}")
    if not isinstance(data["tags"], list) or not all(isinstance(t, str) for t in data["tags"]):
        errors.append("tags must be a list of strings")
    elif len(data["tags"]) > MAX_TAGS:
        errors.append(f"tags has {len(data['tags'])} entries; at most {MAX_TAGS}")
    if not isinstance(data["preview"], str) or not re.search(r"\.jpe?g$", data["preview"], re.IGNORECASE):
        errors.append("preview must be a relative path to a .jpg file")
    for key in ("site", "repo"):
        if not isinstance(data[key], str) or not data[key].startswith("http"):
            errors.append(f"{key} must be an http(s) URL")
    if not isinstance(data["pages"], dict) or not all(isinstance(v, str) for v in data["pages"].values()):
        errors.append("pages must be an object of name -> relative path")
    if not isinstance(data["updated"], str) or not DATE_RE.match(data["updated"]):
        errors.append("updated must be YYYY-MM-DD")
    if "engine" in data and not isinstance(data["engine"], str):
        errors.append("engine must be a string")
    if "base_url" in data and data["base_url"] is not None and not isinstance(data["base_url"], str):
        errors.append("base_url must be a string or null")
    return errors


# --- discovery -------------------------------------------------------------

def fetch_json(url: str, timeout: float = 6.0) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310 (public https)
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError):
        return None


def gh_repo_names(owner: str) -> list[str]:
    try:
        out = subprocess.run(
            ["gh", "api", f"users/{owner}/repos", "--paginate", "--jq", ".[].name"],
            capture_output=True, text=True, check=True, timeout=60,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []
    return [n for n in out.split() if n]


def discover(local_root: Path | None, owner: str | None, hidden: set[str], projects: list[str], use_gh: bool = True) -> list[dict]:
    found: dict[str, dict] = {}
    if local_root and Path(local_root).is_dir():
        for child in sorted(Path(local_root).iterdir()):
            if not child.is_dir() or child.name in hidden:
                continue
            manifest = find_manifest(child)
            if manifest:
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                except ValueError as exc:
                    found[child.name] = {"source": str(manifest), "errors": [f"invalid JSON: {exc}"], "manifest": None}
                    continue
                found[child.name] = {"source": str(manifest), "errors": validate_manifest(data), "manifest": data}
    if owner:
        names = gh_repo_names(owner) if use_gh else []
        for name in names or projects:
            if name in hidden or name in found:
                continue
            url = f"https://{owner.lower()}.github.io/{name}/portfolio.json"
            data = fetch_json(url)
            if data is None:
                continue
            found[name] = {"source": url, "errors": validate_manifest(data), "manifest": data}
    return [dict(repo=k, **v) for k, v in found.items()]


# --- preview ---------------------------------------------------------------

def make_preview(src: str, dst: Path, width: int = 1200, height: int = 675, max_kb: int = 300) -> Path:
    from io import BytesIO
    from PIL import Image

    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=10) as resp:  # noqa: S310
            im = Image.open(BytesIO(resp.read()))
    else:
        im = Image.open(src)
    im = im.convert("RGB")
    target = width / height
    w, h = im.size
    if w / h > target:
        new_w = int(h * target)
        im = im.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:
        new_h = int(w / target)
        im = im.crop((0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h))
    im = im.resize((width, height), Image.LANCZOS)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    for quality in (86, 80, 74, 68, 60):
        im.save(dst, "JPEG", quality=quality, optimize=True)
        if dst.stat().st_size <= max_kb * 1024:
            break
    return dst


# --- CLI -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("detect"); p.add_argument("path", nargs="?", default=".")
    p = sub.add_parser("remote"); p.add_argument("path", nargs="?", default=".")
    p = sub.add_parser("validate"); p.add_argument("manifest")
    p = sub.add_parser("discover")
    p.add_argument("--local-root", default=None); p.add_argument("--owner", default=None)
    p.add_argument("--hidden", default=""); p.add_argument("--projects", default=""); p.add_argument("--no-gh", action="store_true")
    p = sub.add_parser("preview"); p.add_argument("src"); p.add_argument("dst")
    args = parser.parse_args(argv)

    if args.cmd == "detect":
        print(detect_role(Path(args.path)))
        return 0
    if args.cmd == "remote":
        remote = git_remote(Path(args.path))
        if not remote:
            print("no GitHub remote found; pass owner and repo by hand", file=sys.stderr)
            return 1
        print(json.dumps({"owner": remote.owner, "repo": remote.repo, "hub_url": remote.hub_url,
                          "project_url": remote.project_url, "repo_url": remote.repo_url}, indent=2))
        return 0
    if args.cmd == "validate":
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        errors = validate_manifest(data)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("valid" if not errors else f"{len(errors)} error(s)")
        return 1 if errors else 0
    if args.cmd == "discover":
        owner = args.owner
        if not owner:
            remote = git_remote(Path("."))
            owner = remote.owner if remote else None
        hidden = {h for h in args.hidden.split(",") if h}
        projects = [n for n in args.projects.split(",") if n]
        result = discover(Path(args.local_root) if args.local_root else None, owner, hidden, projects, use_gh=not args.no_gh)
        print(json.dumps(result, indent=2))
        return 0
    if args.cmd == "preview":
        out = make_preview(args.src, Path(args.dst))
        print(f"{out} ({out.stat().st_size // 1024} KB)")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
