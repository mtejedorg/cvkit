from pathlib import Path

import fitz
import pytest

from cvtool.compile import build_html, compile_markdown, find_edge

FIXTURES = Path(__file__).parent / "fixtures"
LONG_CV = FIXTURES / "long_cv.md"
SHORT_LETTER = FIXTURES / "short_letter.md"


def _edge_available() -> bool:
    try:
        find_edge()
        return True
    except SystemExit:
        return False


needs_edge = pytest.mark.skipif(not _edge_available(), reason="Microsoft Edge not installed")


def test_build_html_uses_a4_page_rule():
    html = build_html(LONG_CV.read_text(encoding="utf-8"))
    assert "size: A4" in html
    assert "page_height" not in html
    assert "<h1>Alex Rivera</h1>" in html


def test_build_html_keeps_private_spans_by_default():
    html = build_html(SHORT_LETTER.read_text(encoding="utf-8"))
    assert "+1 (555) 010-0142" in html


def test_build_html_public_strips_private_spans_and_separators():
    html = build_html(SHORT_LETTER.read_text(encoding="utf-8"), public=True)
    assert "010-0142" not in html
    assert "class=\"private\"" not in html
    assert "· ·" not in html
    assert "alex.rivera@example.com · linkedin.com/in/alexrivera" in html


def test_build_html_wraps_role_lines_in_cv_role_rows():
    html = build_html(LONG_CV.read_text(encoding="utf-8"))
    assert 'class="cv-role"' in html
    assert 'class="cv-role-dates"' in html
    assert "2021 – Present, Austin, TX" in html


def test_label_rows_before_a_role_line_are_not_swallowed():
    md = (
        "## Skills\n\n**Languages:** Go, Python\n\n**Tools:** Git\n\n## Education\n\n"
        "**B.S. in Computer Science | Example State University** *(2011 – 2015, Austin, TX)*\n\nCapstone: a key-value store.\n"
    )
    html = build_html(md)
    assert html.count('class="cv-role"') == 1
    assert "<p><strong>Languages:</strong> Go, Python</p>" in html
    assert "<p><strong>Tools:</strong> Git</p>" in html
    assert '<span class="cv-role-dates">2011 – 2015, Austin, TX</span>' in html


@needs_edge
def test_long_fixture_paginates_without_splitting_a_role_heading(tmp_path: Path):
    pdf = compile_markdown(LONG_CV, tmp_path / "long.pdf")
    doc = fitz.open(pdf)
    assert doc.page_count >= 2
    assert abs(doc[0].rect.width - 595) < 2 and abs(doc[0].rect.height - 842) < 2
    for page in doc:
        blocks = [b[4].strip() for b in page.get_text("blocks") if b[4].strip()]
        last = blocks[-1]
        # A role line ends with a closing parenthesis of its dates; it must not be the last block on a page.
        assert not (last.endswith(")") and "|" in last), f"role heading orphaned at page end: {last!r}"
    doc.close()


@needs_edge
def test_short_letter_is_one_page(tmp_path: Path):
    pdf = compile_markdown(SHORT_LETTER, tmp_path / "letter.pdf")
    doc = fitz.open(pdf)
    assert doc.page_count == 1
    doc.close()


@needs_edge
def test_missing_photo_does_not_fail_compile(tmp_path: Path):
    md = tmp_path / "photo.md"
    md.write_text(
        LONG_CV.read_text(encoding="utf-8").replace(
            "  </div>\n</div>",
            '  </div>\n  <img src="file:///C:/nope/missing.jpg" class="profile-photo" />\n</div>',
            1,
        ),
        encoding="utf-8",
    )
    pdf = compile_markdown(md, tmp_path / "photo.pdf")
    assert pdf.exists()


@needs_edge
def test_public_pdf_has_no_phone(tmp_path: Path):
    pdf = compile_markdown(SHORT_LETTER, tmp_path / "letter_public.pdf", public=True)
    text = fitz.open(pdf)[0].get_text()
    assert "010-0142" not in text
    assert "alex.rivera@example.com" in text
