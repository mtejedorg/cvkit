"""Locate the workspace that holds `_private/` (profile) and `_generated/` (applications).

Precedence: the CV_WORKSPACE environment variable, then the `workspace` key of
`cv-builder.config.json` next to the skill, then the repository root itself.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

CONFIG_FILENAME = "cv-builder.config.json"
ENV_VAR = "CV_WORKSPACE"


@dataclass(frozen=True)
class Workspace:
    root: Path
    source: str  # "env" | "config" | "default"

    @property
    def private_dir(self) -> Path:
        return self.root / "_private"

    @property
    def generated_dir(self) -> Path:
        return self.root / "_generated"


def resolve_workspace(repo_root: Path, env: Mapping[str, str] | None = None) -> Workspace:
    env = os.environ if env is None else env
    repo_root = Path(repo_root)

    from_env = env.get(ENV_VAR)
    if from_env:
        return Workspace(Path(from_env).expanduser(), "env")

    config_path = repo_root / CONFIG_FILENAME
    if config_path.is_file():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        target = data.get("workspace")
        if target:
            return Workspace(Path(target).expanduser(), "config")

    return Workspace(repo_root, "default")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent
