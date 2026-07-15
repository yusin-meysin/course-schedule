from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Note, ProjectState, Snippet, Task
from .storage import load_state, save_state



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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "demo":
        state = demo_state()
        print(json.dumps(state.to_dict() if hasattr(state, "to_dict") else {"notes": len(state.notes)}, ensure_ascii=False, sort_keys=True))
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
