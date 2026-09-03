import logging
import sys
from pathlib import Path

from triangle import calculate_triangle


def main() -> None:

    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "file_txt.log", encoding="utf-8"),
        ],
        force=True,
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    print("Лабораторная работа №1 — Вариант 1")
    print("Введите длины трёх сторон треугольника.")

    side_a = input("Сторона A: ")
    side_b = input("Сторона B: ")
    side_c = input("Сторона C: ")

    triangle_type, coordinates = calculate_triangle(side_a, side_b, side_c)

    print(f"Тип треугольника: {triangle_type}")
    print(f"Координаты вершин: {coordinates}")


if __name__ == "__main__":
    main()
