from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from habits.core import Habit


def load_habits(path: Path) -> list[Habit]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    return [
        Habit(
            name=item["name"],
            description=item["description"],
            frequency=item["frequency"],
            start_date=date.fromisoformat(item["start_date"]),
            completed_dates=[
                date.fromisoformat(completed) for completed in item["completed_dates"]
            ],
        )
        for item in data
    ]


def save_habits(path: Path, habits: list[Habit]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [
        {
            "name": habit.name,
            "description": habit.description,
            "frequency": habit.frequency,
            "start_date": habit.start_date.isoformat(),
            "completed_dates": [completed.isoformat() for completed in habit.completed_dates],
        }
        for habit in habits
    ]
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
