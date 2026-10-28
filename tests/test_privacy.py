from pathlib import Path

from cvtool.privacy import load_patterns, scan_paths, scan_text


def test_load_patterns_skips_comments_and_blanks(tmp_path: Path):
    f = tmp_path / "patterns.txt"
    f.write_text("# a comment\n\nRivera\nalex.rivera@example.com\n  \n", encoding="utf-8")
    assert load_patterns(f) == ["Rivera", "alex.rivera@example.com"]


def test_single_word_pattern_is_whole_word():
    hits = scan_text("Riverage is a town.\nAlex Rivera lives there.\n", ["Rivera"])
    assert hits == [("Rivera", 2)]


def test_email_pattern_matches_anywhere_case_insensitively():
    hits = scan_text("Contact: ALEX.RIVERA@EXAMPLE.COM today", ["alex.rivera@example.com"])
    assert hits == [("alex.rivera@example.com", 1)]


def test_phone_pattern_matches_as_substring():
    hits = scan_text("Call +1 (555) 010-0142 now", ["555) 010-0142"])
    assert hits == [("555) 010-0142", 1)]


def test_binary_files_are_skipped(tmp_path: Path):
    binary = tmp_path / "photo.jpg"
    binary.write_bytes(b"\xff\xd8\x00Rivera\x00")
    text = tmp_path / "note.md"
    text.write_text("Rivera was here", encoding="utf-8")
    hits = scan_paths([binary, text], ["Rivera"])
    assert [(h.path.name, h.line, h.pattern) for h in hits] == [("note.md", 1, "Rivera")]


def test_missing_patterns_file_returns_empty(tmp_path: Path):
    assert load_patterns(tmp_path / "nope.txt") == []


def _git(repo: Path, *args: str) -> None:
    import subprocess

    subprocess.run(
        ["git", "-c", "user.name=Alex", "-c", "user.email=alex@users.noreply.example.com", "-c", "commit.gpgsign=false", *args],
        cwd=repo, check=True, capture_output=True,
    )


def test_history_finds_content_removed_by_a_later_commit(tmp_path: Path):
    from cvtool.privacy import scan_history

    _git(tmp_path, "init", "-q")
    (tmp_path / "note.md").write_text("Reach me at alex.rivera@example.com\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "first")
    (tmp_path / "note.md").write_text("Reach me through the site\n", encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "remove contact")

    hits, addresses = scan_history(tmp_path, ["alex.rivera@example.com"])
    # once where it was added, once where it was removed
    assert [(h.where, h.pattern) for h in hits] == [("diff", "alex.rivera@example.com")] * 2
    assert addresses == ["alex@users.noreply.example.com"]


def test_history_checks_author_and_message(tmp_path: Path):
    import subprocess

    from cvtool.privacy import scan_history

    _git(tmp_path, "init", "-q")
    (tmp_path / "a.txt").write_text("clean\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    subprocess.run(
        ["git", "-c", "user.name=Alex", "-c", "user.email=alex.rivera@example.com", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "ship it"],
        cwd=tmp_path, check=True, capture_output=True,
    )
    hits, addresses = scan_history(tmp_path, ["alex.rivera@example.com"])
    assert {h.where for h in hits} == {"metadata"}
    assert addresses == ["alex.rivera@example.com"]


def test_history_of_a_clean_repo_has_no_hits(tmp_path: Path):
    from cvtool.privacy import scan_history

    _git(tmp_path, "init", "-q")
    (tmp_path / "a.txt").write_text("clean\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "ok")
    assert scan_history(tmp_path, ["alex.rivera@example.com"])[0] == []


def test_history_ignores_other_branches_unless_all_refs(tmp_path: Path):
    from cvtool.privacy import scan_history

    _git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "a.txt").write_text("clean\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "ok")
    _git(tmp_path, "checkout", "-q", "-b", "old")
    (tmp_path / "a.txt").write_text("alex.rivera@example.com\n", encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "leak")
    _git(tmp_path, "checkout", "-q", "main")
    assert scan_history(tmp_path, ["alex.rivera@example.com"])[0] == []
    assert scan_history(tmp_path, ["alex.rivera@example.com"], all_refs=True)[0]
