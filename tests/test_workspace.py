import json
from pathlib import Path

from cvtool.workspace import resolve_workspace


def test_default_falls_back_to_repo_root(tmp_path: Path):
    ws = resolve_workspace(tmp_path, env={})
    assert ws.root == tmp_path
    assert ws.private_dir == tmp_path / "_private"
    assert ws.generated_dir == tmp_path / "_generated"
    assert ws.source == "default"


def test_config_file_wins_over_default(tmp_path: Path):
    target = tmp_path / "elsewhere"
    (tmp_path / "cvkit.config.json").write_text(
        json.dumps({"workspace": str(target)}), encoding="utf-8"
    )
    ws = resolve_workspace(tmp_path, env={})
    assert ws.root == target
    assert ws.source == "config"


def test_env_wins_over_config(tmp_path: Path):
    (tmp_path / "cvkit.config.json").write_text(
        json.dumps({"workspace": str(tmp_path / "from_config")}), encoding="utf-8"
    )
    env_target = tmp_path / "from_env"
    ws = resolve_workspace(tmp_path, env={"CV_WORKSPACE": str(env_target)})
    assert ws.root == env_target
    assert ws.source == "env"
