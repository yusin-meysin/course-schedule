from __future__ import annotations

from .models import Note, ProjectState, Task, generate_short_id, utc_now
from .validation import normalize_tags, require_text, validate_task_priority, validate_task_status

def create_note(state: ProjectState, title: str, body: str, tags: list[str] | None = None) -> Note:
    now = utc_now()
    note = Note(
        id=generate_short_id("note", {note.id for note in state.notes}),
        title=require_text(title, "title"),
        body=body,
        tags=normalize_tags(tags),
        created_at=now,
        updated_at=now,
    )
    state.notes.append(note)
    return note


def list_notes(state: ProjectState, include_archived: bool = False) -> list[Note]:
    return [note for note in state.notes if include_archived or not note.archived]

def get_note(state: ProjectState, note_id: str) -> Note:
    for note in state.notes:
        if note.id == note_id:
            return note
    raise ValueError(f"Unknown note ID: {note_id}")


def update_note(
    state: ProjectState,
    note_id: str,
    title: str | None = None,
    body: str | None = None,
    tags: list[str] | None = None,
) -> Note:
    note = get_note(state, note_id)
    if title is not None:
        note.title = require_text(title, "title")
    if body is not None:
        note.body = body
    if tags is not None:
        note.tags = normalize_tags(tags)
    note.updated_at = utc_now()
    return note

def archive_note(state: ProjectState, note_id: str) -> Note:
    note = get_note(state, note_id)
    note.archived = True
    note.updated_at = utc_now()
    return note


def restore_note(state: ProjectState, note_id: str) -> Note:
    note = get_note(state, note_id)
    note.archived = False
    note.updated_at = utc_now()
    return note

def create_task(
    state: ProjectState,
    title: str,
    priority: str = "normal",
    owner: str = "",
    due_date: str = "",
    tags: list[str] | None = None,
) -> Task:
    now = utc_now()
    task = Task(
        id=generate_short_id("task", {task.id for task in state.tasks}),
        title=require_text(title, "title"),
        priority=validate_task_priority(priority),
        owner=owner,
        due_date=due_date,
        tags=normalize_tags(tags),
        created_at=now,
        updated_at=now,
    )
    state.tasks.append(task)
    return task


def list_tasks(state: ProjectState) -> list[Task]:
    return list(state.tasks)

def get_task(state: ProjectState, task_id: str) -> Task:
    for task in state.tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"Unknown task ID: {task_id}")


def update_task_status(state: ProjectState, task_id: str, status: str) -> Task:
    task = get_task(state, task_id)
    task.status = validate_task_status(status)
    task.updated_at = utc_now()
    return task

