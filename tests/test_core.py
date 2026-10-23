from datetime import date, timedelta

import pytest

from habits.core import Habit, create_habit, current_streak, mark_habit_done


def test_create_habit_requires_all_fields() -> None:
    habit = create_habit(
        [],
        name="Leer",
        description="Leer apuntes",
        frequency="daily",
        start_date=date(2026, 10, 20),
    )

    assert habit.name == "Leer"
    assert habit.description == "Leer apuntes"
    assert habit.frequency == "daily"
    assert habit.start_date == date(2026, 10, 20)
    assert habit.completed_dates == []


def test_habit_model_stores_all_fields_and_defaults_completions() -> None:
    habit = Habit(
        name="Repasar",
        description="Repasar matemáticas",
        frequency="daily",
        start_date=date(2026, 10, 20),
    )

    assert habit.name == "Repasar"
    assert habit.description == "Repasar matemáticas"
    assert habit.frequency == "daily"
    assert habit.start_date == date(2026, 10, 20)
    assert habit.completed_dates == []


def test_create_habit_rejects_duplicate_name() -> None:
    habits = [
        create_habit(
            [],
            name="Leer",
            description="Leer apuntes",
            frequency="daily",
            start_date=date(2026, 10, 20),
        )
    ]

    with pytest.raises(ValueError, match="ya existe"):
        create_habit(
            habits,
            name="Leer",
            description="Otra descripción",
            frequency="daily",
            start_date=date(2026, 10, 20),
        )


def test_create_habit_rejects_future_start_date() -> None:
    with pytest.raises(ValueError, match="futura"):
        create_habit(
            [],
            name="Leer",
            description="Leer apuntes",
            frequency="daily",
            start_date=date(2026, 10, 24),
            today=date(2026, 10, 23),
        )


def test_mark_habit_done_records_today_only_once() -> None:
    today = date(2026, 10, 23)
    habit = create_habit(
        [],
        name="Leer",
        description="Leer apuntes",
        frequency="daily",
        start_date=today,
    )

    mark_habit_done([habit], "Leer", today)

    assert habit.completed_dates == [today]
    with pytest.raises(ValueError, match="marcado"):
        mark_habit_done([habit], "Leer", today)


def test_mark_habit_done_rejects_unknown_habit() -> None:
    with pytest.raises(ValueError, match="no existe"):
        mark_habit_done([], "Leer", date(2026, 10, 23))


def test_current_streak_counts_consecutive_days_ending_today() -> None:
    today = date(2026, 10, 23)
    habit = create_habit(
        [],
        name="Leer",
        description="Leer apuntes",
        frequency="daily",
        start_date=today - timedelta(days=3),
    )
    habit.completed_dates = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]

    assert current_streak(habit, today) == 3
    assert current_streak(habit, today + timedelta(days=1)) == 0
