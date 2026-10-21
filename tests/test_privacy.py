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
