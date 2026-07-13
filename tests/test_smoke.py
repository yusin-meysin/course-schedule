from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from course_schedule.cli import main
from course_schedule.models import Note, ProjectState, Task
from course_schedule.storage import load_state, save_state


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


if __name__ == "__main__":
    unittest.main()
