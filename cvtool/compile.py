"""Markdown -> HTML (A4 template) -> PDF through headless Microsoft Edge.

Pages are real A4 pages with print margins; CSS break rules keep a role title
with its first bullets. `public=True` strips every `<span class="private">`
(the phone number, by convention) so one Markdown source yields both the PDF
you send to a recruiter and the one you can put on a website.
"""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
HTML_TEMPLATE = TEMPLATES_DIR / "cv_a4.html"
CSS_TEMPLATE = TEMPLATES_DIR / "cv_a4.css"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/microsoft-edge",
    "/usr/bin/microsoft-edge-stable",
]

_PRIVATE_SPAN = re.compile(r'<span class="private">.*?</span>', re.DOTALL)
_ROLE_LINE = re.compile(
    r"<p><strong>(?P<title>.+?)</strong>(?P<rest>[^<]*?)<em>\((?P<dates>.+?)\)</em>\s*</p>",
    re.DOTALL,
)
_LOCAL_IMG = re.compile(r'<img[^>]*src="file:///(?P<path>[^"]+)"[^>]*>')


def find_edge() -> str:
    candidates = [os.environ.get("EDGE_PATH"), *EDGE_CANDIDATES]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    raise SystemExit("Microsoft Edge not found. Set EDGE_PATH to your msedge executable.")


def _strip_private(html: str) -> str:
    html = _PRIVATE_SPAN.sub("", html)
    html = re.sub(r"(\s*[·|]\s*){2,}", lambda m: f" {m.group(0).strip()[0]} ", html)
    html = re.sub(r'(class="cv-contact">)\s*[·|]\s*', r"\1", html)
    html = re.sub(r"\s*[·|]\s*(</p>)", r"\1", html)
    return html


def _wrap_roles(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        title = m.group("title") + m.group("rest").rstrip()
        return (
            '<div class="cv-role"><span class="cv-role-title"><strong>'
            f'{title}</strong></span><span class="cv-role-dates">{m.group("dates")}</span></div>'
        )

    return _ROLE_LINE.sub(repl, html)


def build_html(md_text: str, *, public: bool = False) -> str:
    body = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    body = _wrap_roles(body)
    if public:
        body = _strip_private(body)
    css = CSS_TEMPLATE.read_text(encoding="utf-8")
    skeleton = HTML_TEMPLATE.read_text(encoding="utf-8")
    return skeleton.replace("{css}", css).replace("{content}", body)


def _drop_missing_images(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        raw = m.group("path").replace("%20", " ")
        if os.path.exists(raw) or os.path.exists("/" + raw):
            return m.group(0)
        print(f"  Warning: image not found, omitted: {raw}", file=sys.stderr)
        return ""

    return _LOCAL_IMG.sub(repl, html)


def compile_markdown(md_path: Path, pdf_path: Path, *, public: bool = False, edge_path: str | None = None) -> Path:
    md_path, pdf_path = Path(md_path), Path(pdf_path)
    edge_path = edge_path or find_edge()
    html = _drop_missing_images(build_html(md_path.read_text(encoding="utf-8"), public=public))

    html_path = pdf_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    profile_dir = os.path.join(tempfile.gettempdir(), "edge_headless_pdf")
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile_dir}",
        f"--print-to-pdf={pdf_path.resolve()}",
        pathlib.Path(html_path).resolve().as_uri(),
    ]
    try:
        subprocess.run(cmd, check=True, timeout=45, capture_output=True)
    finally:
        if html_path.exists():
            html_path.unlink()
    if not pdf_path.exists():
        raise RuntimeError(f"Edge produced no PDF for {md_path}")
    return pdf_path


def compile_folder(folder: Path, *, force: bool = False, public: bool = False, edge_path: str | None = None) -> list[Path]:
    folder = Path(folder)
    edge_path = edge_path or find_edge()
    outputs: list[Path] = []
    for md_path in sorted(folder.glob("*.md")):
        suffix = "_public.pdf" if public else ".pdf"
        pdf_path = md_path.with_name(md_path.stem + suffix)
        if not force and pdf_path.exists() and pdf_path.stat().st_mtime >= md_path.stat().st_mtime:
            continue
        compile_markdown(md_path, pdf_path, public=public, edge_path=edge_path)
        outputs.append(pdf_path)
        print(f"Compiled: {pdf_path}")
    return outputs
