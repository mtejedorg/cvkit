from pathlib import Path

import pytest

from cvtool.compile import compile_markdown, find_edge
from cvtool.verify import verify_pdf

FIXTURES = Path(__file__).parent / "fixtures"
HEADINGS = ["Professional Summary", "Professional Experience", "Core Competencies", "Education"]


def _edge_available() -> bool:
    try:
        find_edge()
        return True
    except SystemExit:
        return False


pytestmark = pytest.mark.skipif(not _edge_available(), reason="Microsoft Edge not installed")


@pytest.fixture(scope="module")
def pdfs(tmp_path_factory):
    out = tmp_path_factory.mktemp("pdfs")
    private = compile_markdown(FIXTURES / "long_cv.md", out / "cv.pdf")
    public = compile_markdown(FIXTURES / "long_cv.md", out / "cv_public.pdf", public=True)
    return private, public


def test_passing_case(pdfs):
    private, _ = pdfs
    issues = verify_pdf(
        private, pages=None, max_pages=3, min_chars=50,
        required_text=["Alex Rivera", "alex.rivera@example.com"], forbidden_text=[], order=HEADINGS,
    )
    assert issues == []


def test_max_pages_violation_is_reported(pdfs):
    private, _ = pdfs
    issues = verify_pdf(private, pages=None, max_pages=1, min_chars=50, required_text=[], forbidden_text=[], order=[])
    assert any("max" in i and "page" in i for i in issues)


def test_forbidden_text_found_in_private_but_not_public(pdfs):
    private, public = pdfs
    assert any("forbidden" in i for i in verify_pdf(private, pages=None, max_pages=None, min_chars=50, required_text=[], forbidden_text=["010-0142"], order=[]))
    assert verify_pdf(public, pages=None, max_pages=None, min_chars=50, required_text=[], forbidden_text=["010-0142"], order=[]) == []


def test_order_violation_is_reported(pdfs):
    private, _ = pdfs
    issues = verify_pdf(private, pages=None, max_pages=None, min_chars=50, required_text=[], forbidden_text=[], order=list(reversed(HEADINGS)))
    assert any("order" in i for i in issues)


def test_missing_order_heading_is_reported(pdfs):
    private, _ = pdfs
    issues = verify_pdf(private, pages=None, max_pages=None, min_chars=50, required_text=[], forbidden_text=[], order=["Professional Summary", "Hobbies"])
    assert any("Hobbies" in i for i in issues)
