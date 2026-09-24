#!/usr/bin/env python3
"""csv-insight - маленький отчёт о CSV-файле.

Учебный проект N1 (Фаза 0). Что демонстрирует:
  * чтение файла и разбор CSV стандартной библиотекой;
  * списки, словари, функции;
  * аккуратную обработку ошибок;
  * аргументы командной строки через argparse.

Запуск:
    python main.py
    python main.py data/sample.csv
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

DEFAULT_FILE = Path("data/sample.csv")


def read_rows(path):
    """Читает CSV и возвращает (имена колонок, список строк-словарей)."""
    if not path.exists():
        raise FileNotFoundError("Файл не найден: " + str(path))

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("В файле нет строки с заголовками колонок.")
        columns = reader.fieldnames
        rows = [row for row in reader]

    if not rows:
        raise ValueError("Файл пустой - нет ни одной строки данных.")

    return columns, rows


def as_number(value):
    """Пробует превратить строку в число. Возвращает float или None."""
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None


def summarize(values):
    """Считает статистику по одной колонке."""
    filled = [v for v in values if v is not None and v.strip() != ""]
    missing = len(values) - len(filled)

    numbers = [as_number(v) for v in filled]
    is_numeric = bool(filled) and all(n is not None for n in numbers)

    if is_numeric:
        nums = [n for n in numbers if n is not None]
        return {
            "type": "числовая",
            "missing": missing,
            "min": min(nums),
            "max": max(nums),
            "mean": sum(nums) / len(nums),
        }

    top = Counter(filled).most_common(3)
    return {
        "type": "текстовая",
        "missing": missing,
        "unique": len(set(filled)),
        "top": top,
    }


def format_value(number):
    """Красиво печатает число: целое или с двумя знаками после точки."""
    if number == int(number):
        return str(int(number))
    return format(number, ".2f")


def print_report(path, columns, rows):
    """Печатает итоговый отчёт в консоль."""
    print()
    print("Отчёт по файлу: " + str(path))
    print("Строк: " + str(len(rows)) + "   Колонок: " + str(len(columns)))
    print("-" * 46)

    for column in columns:
        values = [row.get(column, "") for row in rows]
        info = summarize(values)

        print()
        print("- " + column + "  [" + info["type"] + "]")
        print("    пропусков: " + str(info["missing"]))

        if info["type"] == "числовая":
            print("    минимум: " + format_value(info["min"]))
            print("    максимум: " + format_value(info["max"]))
            print("    среднее: " + format_value(info["mean"]))
        else:
            print("    уникальных значений: " + str(info["unique"]))
            top = ", ".join(value + " (" + str(count) + ")" for value, count in info["top"])
            print("    чаще всего: " + top)

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Показывает краткий отчёт по CSV-файлу."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=str(DEFAULT_FILE),
        help="путь к CSV-файлу (по умолчанию data/sample.csv)",
    )
    args = parser.parse_args()

    try:
        columns, rows = read_rows(Path(args.file))
    except (FileNotFoundError, ValueError) as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return 1

    print_report(args.file, columns, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
