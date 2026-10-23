from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Sequence

from habits.core import create_habit, current_streak, mark_habit_done
from habits.storage import load_habits, save_habits


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Registra hábitos de estudio")
    parser.add_argument("--data", type=Path, default=Path("habits.json"))
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="crea un hábito")
    create.add_argument("name")
    create.add_argument("--description", required=True)
    create.add_argument("--frequency", choices=["daily"], required=True)
    create.add_argument("--start-date", required=True)

    mark = commands.add_parser("mark", help="marca un hábito como hecho hoy")
    mark.add_argument("name")

    commands.add_parser("list", help="lista los hábitos y sus rachas")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    habits = load_habits(args.data)

    try:
        if args.command == "create":
            habit = create_habit(
                habits,
                name=args.name,
                description=args.description,
                frequency=args.frequency,
                start_date=date.fromisoformat(args.start_date),
            )
            habits.append(habit)
            save_habits(args.data, habits)
            print(f"Hábito creado: {habit.name}")
        elif args.command == "mark":
            habit = mark_habit_done(habits, args.name, date.today())
            save_habits(args.data, habits)
            print(f"Hábito marcado como hecho hoy: {habit.name}")
        else:
            if not habits:
                print("No hay hábitos registrados.")
            for habit in sorted(habits, key=lambda item: item.name):
                streak = current_streak(habit, date.today())
                print(
                    f"{habit.name} | {habit.description} | diaria | "
                    f"inicio: {habit.start_date.isoformat()} | racha: {streak}"
                )
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
