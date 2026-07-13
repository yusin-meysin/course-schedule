from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .models import ProjectState


def load_state(path: str | Path) -> ProjectState:
    target = Path(path)
    if not target.exists():
        return ProjectState()
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON state file: {target}") from exc
    return ProjectState.from_dict(data)


def save_state(path: str | Path, state: ProjectState) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, delete=False) as handle:
        handle.write(payload)
        temp_name = handle.name
    os.replace(temp_name, target)
