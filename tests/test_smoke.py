from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from course_schedule.cli import main
from course_schedule.models import Note, ProjectState, Task


class ProjectSmokeTests(unittest.TestCase):
    def test_cli_help(self) -> None:
        self.assertEqual(main([]), 0)

    def test_models_hold_basic_data(self) -> None:
        note = Note(id="note-1", title="Plan")
        task = Task(id="task-1", title="Ship")
        state = ProjectState(notes=[note], tasks=[task])

        self.assertEqual(state.notes[0].title, "Plan")
        self.assertEqual(state.tasks[0].status, "todo")


if __name__ == "__main__":
    unittest.main()
