"""Every SKILL.md must carry frontmatter that parses and a real description.

An unquoted ': ' inside a plain YAML description breaks the whole block. The loader then
drops the description and the skill never triggers, so this guards against it.
"""
import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent / ".claude" / "skills"
SKILL_FILES = sorted(SKILLS.glob("*/SKILL.md"))


def _frontmatter(path: Path) -> str:
    match = re.match(r"---\r?\n(.*?)\r?\n---", path.read_text(encoding="utf-8"), re.S)
    assert match, f"{path} has no frontmatter block"
    return match.group(1)


def test_skill_files_found():
    assert len(SKILL_FILES) >= 3


@pytest.mark.parametrize("path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_description_is_not_a_plain_scalar_with_colon(path):
    """Dependency-free check: a plain description line must not contain ': ' or ' #'."""
    for line in _frontmatter(path).splitlines():
        if line.startswith("description:"):
            value = line[len("description:"):].strip()
            assert value, f"{path.parent.name}: description is empty on its own line"
            if value[0] in ">|\"'":
                return
            assert ": " not in value and " #" not in value, (
                f"{path.parent.name}: description is a plain scalar containing ': ' or ' #'; "
                "fold it with '>-' or quote it"
            )
            return
    pytest.fail(f"{path.parent.name}: no description line")


@pytest.mark.parametrize("path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_frontmatter_parses_and_matches_folder(path):
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load(_frontmatter(path))
    assert data["name"] == path.parent.name
    assert len(data["description"]) > 100
