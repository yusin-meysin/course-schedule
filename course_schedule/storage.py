from __future__ import annotations

from .models import ProjectState


def load_state(path: str) -> ProjectState:
    return ProjectState()
