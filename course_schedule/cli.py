from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Note, ProjectState, Snippet, Task
from .storage import load_state, save_state
from .services import (
    create_note,
    list_notes,
    get_note,
    update_note,
    archive_note,
    restore_note,
    create_task,
    list_tasks,
    get_task,
    update_task_status,
    filter_tasks,
    task_summary_counts,
)



def demo_state() -> ProjectState:
    return ProjectState(
        notes=[Note(id="note-demo", title="CourseSchedule launch", body="Capture a useful idea.", tags=["demo"])],
        tasks=[Task(id="task-demo", title="Review next step", priority="high", owner="me")],
        snippets=[Snippet(id="snippet-demo", title="Hello", language="python", body="print('hello')")],
    )

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="course_schedule")
    parser.add_argument("--data", default="data/state.json")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("demo")
    subparsers.add_parser("summary")
    subparsers.add_parser("notes")
    subparsers.add_parser("tasks")
    subparsers.add_parser("snippets")
    note_add = subparsers.add_parser("note-add")
    note_add.add_argument("--title", required=True)
    note_add.add_argument("--body", default="")
    note_add.add_argument("--tag", action="append", default=[])
    subparsers.add_parser("note-list")
    note_show = subparsers.add_parser("note-show")
    note_show.add_argument("note_id")
    note_update = subparsers.add_parser("note-update")
    note_update.add_argument("note_id")
    note_update.add_argument("--title")
    note_update.add_argument("--body")
    note_update.add_argument("--tag", action="append")
    note_archive = subparsers.add_parser("note-archive")
    note_archive.add_argument("note_id")
    note_restore = subparsers.add_parser("note-restore")
    note_restore.add_argument("note_id")
    task_add = subparsers.add_parser("task-add")
    task_add.add_argument("--title", required=True)
    task_add.add_argument("--priority", default="normal")
    task_add.add_argument("--owner", default="")
    task_add.add_argument("--due-date", default="")
    task_add.add_argument("--tag", action="append", default=[])
    task_list = subparsers.add_parser("task-list")
    task_list.add_argument("--status")
    task_list.add_argument("--owner")
    task_list.add_argument("--priority")
    task_list.add_argument("--tag")
    task_list.add_argument("--due-from")
    task_list.add_argument("--due-to")
    task_status = subparsers.add_parser("task-status")
    task_status.add_argument("task_id")
    task_status.add_argument("status")
    subparsers.add_parser("task-summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "demo":
        state = demo_state()
        print(json.dumps(state.to_dict() if hasattr(state, "to_dict") else {"notes": len(state.notes)}, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "summary":
        state = load_state(args.data) if args.data else demo_state()
        print(f"notes={len(state.notes)} tasks={len(state.tasks)} snippets={len(state.snippets)}")
        return 0
    if args.command == "notes":
        state = load_state(args.data) if args.data else demo_state()
        for note in state.notes:
            print(f"{note.id} {note.title}")
        return 0
    if args.command == "tasks":
        state = load_state(args.data) if args.data else demo_state()
        for task in state.tasks:
            print(f"{task.id} {task.status} {task.title}")
        return 0
    if args.command == "snippets":
        state = load_state(args.data) if args.data else demo_state()
        for snippet in state.snippets:
            print(f"{snippet.id} {snippet.language} {snippet.title}")
        return 0
    if args.command == "note-add":
        state = load_state(args.data)
        note = create_note(state, args.title, args.body, args.tag)
        save_state(args.data, state)
        print(note.id)
        return 0
    if args.command == "note-list":
        state = load_state(args.data)
        for note in list_notes(state):
            print(f"{note.id} {note.title}")
        return 0
    if args.command == "note-show":
        state = load_state(args.data)
        note = get_note(state, args.note_id)
        print(f"{note.id} {note.title}\n{note.body}")
        return 0
    if args.command == "note-update":
        state = load_state(args.data)
        note = update_note(state, args.note_id, args.title, args.body, args.tag)
        save_state(args.data, state)
        print(note.id)
        return 0
    if args.command == "note-archive":
        state = load_state(args.data)
        archive_note(state, args.note_id)
        save_state(args.data, state)
        print(args.note_id)
        return 0
    if args.command == "note-restore":
        state = load_state(args.data)
        restore_note(state, args.note_id)
        save_state(args.data, state)
        print(args.note_id)
        return 0
    if args.command == "task-add":
        state = load_state(args.data)
        task = create_task(state, args.title, args.priority, args.owner, args.due_date, args.tag)
        save_state(args.data, state)
        print(task.id)
        return 0
    if args.command == "task-list":
        state = load_state(args.data)
        tasks = filter_tasks(state, args.status, args.owner, args.priority, args.tag, args.due_from, args.due_to) if "filter_tasks" in globals() else list_tasks(state)
        for task in tasks:
            print(f"{task.id} {task.status} {task.title}")
        return 0
    if args.command == "task-status":
        state = load_state(args.data)
        task = update_task_status(state, args.task_id, args.status)
        save_state(args.data, state)
        print(f"{task.id} {task.status}")
        return 0
    if args.command == "task-summary":
        state = load_state(args.data)
        print(json.dumps(task_summary_counts(state), ensure_ascii=False, sort_keys=True))
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
