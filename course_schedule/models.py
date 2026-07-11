from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


TASK_STATUSES = ("todo", "doing", "blocked", "done")
TASK_PRIORITIES = ("low", "normal", "high")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Note:
    id: str
    title: str
    body: str = ""
    tags: list[str] = field(default_factory=list)
    archived: bool = False
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)


@dataclass
class Task:
    id: str
    title: str
    status: str = "todo"
    priority: str = "normal"
    owner: str = ""
    due_date: str = ""
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(**data)


@dataclass
class Snippet:
    id: str
    title: str
    language: str = "text"
    body: str = ""
    tags: list[str] = field(default_factory=list)
    source: str = ""
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Snippet":
        return cls(**data)


@dataclass
class ProjectState:
    notes: list[Note] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    snippets: list[Snippet] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "notes": [note.to_dict() for note in self.notes],
            "tasks": [task.to_dict() for task in self.tasks],
            "snippets": [snippet.to_dict() for snippet in self.snippets],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectState":
        return cls(
            notes=[Note.from_dict(item) for item in data.get("notes", [])],
            tasks=[Task.from_dict(item) for item in data.get("tasks", [])],
            snippets=[Snippet.from_dict(item) for item in data.get("snippets", [])],
        )

