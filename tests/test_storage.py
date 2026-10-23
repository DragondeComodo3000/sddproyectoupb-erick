from datetime import date

from habits.core import Habit
from habits.storage import load_habits, save_habits


def test_save_and_load_preserves_habit_data(tmp_path) -> None:
    path = tmp_path / "habits.json"
    habits = [
        Habit(
            name="Leer",
            description="Leer apuntes",
            frequency="daily",
            start_date=date(2026, 10, 20),
            completed_dates=[date(2026, 10, 23)],
        )
    ]

    save_habits(path, habits)

    assert load_habits(path) == habits
