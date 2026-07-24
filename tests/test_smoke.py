from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from course_schedule.cli import main
from course_schedule.models import Note, ProjectState, Task
from course_schedule.cli import demo_state
from course_schedule.storage import load_state, save_state
from course_schedule.models import generate_short_id
from course_schedule.validation import normalize_tags, require_text, validate_task_status
from course_schedule.services import (
    create_note,
    list_notes,
    get_note,
    update_note,
)


class ProjectSmokeTests(unittest.TestCase):
    def test_cli_help(self) -> None:
        self.assertEqual(main([]), 0)

    def test_models_hold_basic_data(self) -> None:
        note = Note(id="note-1", title="Plan")
        task = Task(id="task-1", title="Ship")
        state = ProjectState(notes=[note], tasks=[task])

        self.assertEqual(state.notes[0].title, "Plan")
        self.assertEqual(state.tasks[0].status, "todo")

    def test_state_round_trip(self) -> None:
        state = ProjectState(notes=[Note(id="n1", title="One")], tasks=[Task(id="t1", title="Two")])
        restored = ProjectState.from_dict(state.to_dict())

        self.assertEqual(restored.notes[0].title, "One")
        self.assertEqual(restored.tasks[0].title, "Two")

    def test_storage_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            save_state(path, ProjectState(notes=[Note(id="n1", title="Saved")]))

            loaded = load_state(path)

        self.assertEqual(loaded.notes[0].title, "Saved")

    def test_demo_state_has_records(self) -> None:
        state = demo_state()

        self.assertGreaterEqual(len(state.notes), 1)
        self.assertGreaterEqual(len(state.tasks), 1)

    def test_generate_short_id_uses_prefix(self) -> None:
        generated = generate_short_id("note", size=6)

        self.assertTrue(generated.startswith("note-"))

    def test_validation_helpers(self) -> None:
        self.assertEqual(normalize_tags([" Work ", "work", "Bug"]), ["work", "bug"])
        self.assertEqual(require_text(" Title ", "title"), "Title")
        self.assertEqual(validate_task_status("todo"), "todo")
        with self.assertRaises(ValueError):
            require_text(" ", "title")

    def test_create_and_list_notes(self) -> None:
        state = ProjectState()
        note = create_note(state, " New note ", "Body", ["Work", "work"])

        self.assertEqual(note.title, "New note")
        self.assertEqual(note.tags, ["work"])
        self.assertEqual(list_notes(state), [note])

    def test_get_and_update_note(self) -> None:
        state = ProjectState()
        note = create_note(state, "Old", "Body")

        update_note(state, note.id, title="New", tags=["A", "a"])

        self.assertEqual(get_note(state, note.id).title, "New")
        with self.assertRaises(ValueError):
            get_note(state, "missing")


if __name__ == "__main__":
    unittest.main()
