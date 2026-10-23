from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Habit:
    name: str
    description: str
    frequency: str
    start_date: date
    completed_dates: list[date] = field(default_factory=list)


def create_habit(
    habits: list[Habit],
    *,
    name: str,
    description: str,
    frequency: str,
    start_date: date,
    today: date | None = None,
) -> Habit:
    if not name.strip():
        raise ValueError("el nombre es obligatorio")
    if not description.strip():
        raise ValueError("la descripción es obligatoria")
    if frequency != "daily":
        raise ValueError("la frecuencia debe ser diaria")
    if today is None:
        today = date.today()
    if start_date > today:
        raise ValueError("la fecha de inicio no puede ser futura")
    if any(habit.name == name for habit in habits):
        raise ValueError("ya existe un hábito con ese nombre")
    return Habit(name, description, frequency, start_date)


def mark_habit_done(habits: list[Habit], name: str, today: date) -> Habit:
    habit = next((item for item in habits if item.name == name), None)
    if habit is None:
        raise ValueError("el hábito no existe")
    if today in habit.completed_dates:
        raise ValueError("el hábito ya está marcado como hecho hoy")
    habit.completed_dates.append(today)
    habit.completed_dates.sort()
    return habit


def current_streak(habit: Habit, today: date) -> int:
    completed = set(habit.completed_dates)
    if today not in completed:
        return 0
    streak = 0
    day = today
    while day in completed:
        streak += 1
        day -= timedelta(days=1)
    return streak
