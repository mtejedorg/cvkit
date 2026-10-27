import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".claude" / "skills" / "portfolio" / "scripts"))
import portfolio_tool as pt  # noqa: E402

GOOD = {
    "schema": 1, "name": "Example Game", "slug": "example-game", "status": "in development", "engine": "Godot 4",
    "blurb": "A 2.5D beat-driven action roguelite. Built solo with AI coding agents.", "tags": ["Godot 4", "GDScript"],
    "preview": "assets/preview.jpg", "site": "https://example.github.io/example-game/",
    "repo": "https://github.com/example/example-game", "pages": {"mechanics": "mechanics.html", "tech": "tech.html"},
    "updated": "2026-10-27",
}


@pytest.mark.parametrize("url", [
    "git@github.com:Example/example-game.git",
    "https://github.com/Example/example-game.git",
    "https://github.com/Example/example-game",
    "ssh://git@github.com/Example/example-game.git",
])
def test_parse_remote_forms(url):
    r = pt.parse_remote(url)
    assert (r.owner, r.repo) == ("Example", "example-game")
    assert r.project_url == "https://example.github.io/example-game/"
    assert r.hub_url == "https://example.github.io/"
    assert r.repo_url == "https://github.com/Example/example-game"


def test_parse_remote_rejects_other_hosts():
    assert pt.parse_remote("https://gitlab.com/x/y.git") is None


def test_detect_role(tmp_path: Path):
    assert pt.detect_role(tmp_path) == "none"
    (tmp_path / "docs" / "site").mkdir(parents=True)
    (tmp_path / "docs" / "site" / "portfolio.json").write_text("{}", encoding="utf-8")
    assert pt.detect_role(tmp_path) == "project"
    (tmp_path / "portfolio.hub.json").write_text("{}", encoding="utf-8")
    assert pt.detect_role(tmp_path) == "hub"


def test_validate_good_manifest():
    assert pt.validate_manifest(GOOD) == []


def test_validate_reports_each_rule():
    bad = dict(GOOD, slug="Bad Slug", status="done", tags=list("abcdef"), updated="27/10/2026", extra=1,
               blurb=" ".join(["word"] * 50))
    errors = pt.validate_manifest(bad)
    joined = "\n".join(errors)
    assert "unknown key: extra" in joined
    bad.pop("extra")
    errors = pt.validate_manifest(bad)
    joined = "\n".join(errors)
    for needle in ("slug", "status", "tags has 6", "blurb has 50", "updated"):
        assert needle in joined, needle


def test_validate_missing_keys():
    errors = pt.validate_manifest({"schema": 1})
    assert any(e.startswith("missing key: name") for e in errors)


def test_discover_local_only(tmp_path: Path):
    root = tmp_path / "repos"
    good = root / "example-game" / "docs" / "site"; good.mkdir(parents=True)
    good.joinpath("portfolio.json").write_text(json.dumps(GOOD), encoding="utf-8")
    broken = root / "broken" / "site"; broken.mkdir(parents=True)
    broken.joinpath("portfolio.json").write_text("{not json", encoding="utf-8")
    hidden = root / "hidden-one" / "docs" / "site"; hidden.mkdir(parents=True)
    hidden.joinpath("portfolio.json").write_text(json.dumps(GOOD), encoding="utf-8")
    (root / "plain-repo").mkdir()

    found = pt.discover(root, owner=None, hidden={"hidden-one"}, projects=[], use_gh=False)
    by_repo = {f["repo"]: f for f in found}
    assert set(by_repo) == {"example-game", "broken"}
    assert by_repo["example-game"]["errors"] == []
    assert by_repo["example-game"]["manifest"]["slug"] == "example-game"
    assert by_repo["broken"]["manifest"] is None and "invalid JSON" in by_repo["broken"]["errors"][0]


def test_discover_remote_uses_projects_list_without_gh(tmp_path: Path, monkeypatch):
    calls = []

    def fake_fetch(url, timeout=6.0):
        calls.append(url)
        return GOOD if url.endswith("/example-game/portfolio.json") else None

    monkeypatch.setattr(pt, "fetch_json", fake_fetch)
    found = pt.discover(None, owner="Example", hidden=set(), projects=["example-game", "other"], use_gh=False)
    assert [f["repo"] for f in found] == ["example-game"]
    assert calls == ["https://example.github.io/example-game/portfolio.json", "https://example.github.io/other/portfolio.json"]


def test_preview_is_1200x675_jpeg(tmp_path: Path):
    from PIL import Image
    src = tmp_path / "wide.png"
    Image.new("RGB", (1920, 1080), (30, 90, 200)).save(src)
    out = pt.make_preview(str(src), tmp_path / "preview.jpg")
    im = Image.open(out)
    assert im.size == (1200, 675) and im.format == "JPEG"
    assert out.stat().st_size <= 300 * 1024
