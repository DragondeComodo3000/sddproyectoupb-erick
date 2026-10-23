from datetime import date

from habits.cli import main


def test_cli_can_create_mark_and_list_habit(tmp_path, capsys) -> None:
    path = tmp_path / "habits.json"
    today = date.today().isoformat()

    assert main(
        [
            "--data",
            str(path),
            "create",
            "Leer",
            "--description",
            "Leer apuntes",
            "--frequency",
            "daily",
            "--start-date",
            today,
        ]
    ) == 0
    assert main(["--data", str(path), "mark", "Leer"]) == 0
    assert main(["--data", str(path), "list"]) == 0

    output = capsys.readouterr().out
    assert "Hábito creado: Leer" in output
    assert "Hábito marcado como hecho hoy: Leer" in output
    assert "Leer | Leer apuntes | diaria" in output
    assert "racha: 1" in output


def test_cli_rejects_duplicate_habit(tmp_path, capsys) -> None:
    path = tmp_path / "habits.json"
    today = date.today().isoformat()
    arguments = [
        "--data",
        str(path),
        "create",
        "Leer",
        "--description",
        "Leer apuntes",
        "--frequency",
        "daily",
        "--start-date",
        today,
    ]

    assert main(arguments) == 0
    assert main(arguments) == 1
    assert "Error:" in capsys.readouterr().err
