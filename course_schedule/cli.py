from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Note, ProjectState, Snippet, Task
from .storage import load_state, save_state
from .services import (
    create_note,
    list_notes,
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
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
