import logging
import math
from typing import List, Tuple

Coordinates = List[Tuple[int, int]]

NUMERIC_ERROR_COORDINATES: Coordinates = [(-1, -1), (-1, -1), (-1, -1)]
NON_NUMERIC_ERROR_COORDINATES: Coordinates = [(-2, -2), (-2, -2), (-2, -2)]


def _parse_positive_float(value: str, side_name: str) -> float:

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Сторона {side_name} должна быть вещественным числом") from exc

    if not math.isfinite(number):
        raise ArithmeticError(f"Сторона {side_name} должна быть конечным числом")

    if number <= 0:
        raise ArithmeticError(f"Сторона {side_name} должна быть положительным числом")

    return number


def _triangle_type(a: float, b: float, c: float) -> str:

    equal_ab = math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    equal_bc = math.isclose(b, c, rel_tol=1e-9, abs_tol=1e-12)
    equal_ac = math.isclose(a, c, rel_tol=1e-9, abs_tol=1e-12)

    if equal_ab and equal_bc:
        return "равносторонний"
    if equal_ab or equal_bc or equal_ac:
        return "равнобедренный"
    return "разносторонний"


def _calculate_coordinates(a: float, b: float, c: float) -> Coordinates:

    x = (b * b + c * c - a * a) / (2.0 * c)
    y_squared = b * b - x * x


    if y_squared < 0 and math.isclose(y_squared, 0.0, abs_tol=1e-10):
        y_squared = 0.0

    if y_squared <= 0:
        raise ArithmeticError("Невозможно вычислить ненулевую высоту треугольника")

    y = math.sqrt(y_squared)

    raw_points = [(0.0, 0.0), (c, 0.0), (x, y)]
    min_x = min(point[0] for point in raw_points)
    max_x = max(point[0] for point in raw_points)
    min_y = min(point[1] for point in raw_points)
    max_y = max(point[1] for point in raw_points)

    width = max_x - min_x
    height = max_y - min_y

    margin = 5
    available = 100 - 2 * margin
    scale_x = available / width if width > 0 else 1.0
    scale_y = available / height if height > 0 else 1.0
    scale = min(scale_x, scale_y)

    scaled_width = width * scale
    scaled_height = height * scale

    offset_x = margin + (available - scaled_width) / 2.0 - min_x * scale
    offset_y = margin + (available - scaled_height) / 2.0 - min_y * scale

    result: Coordinates = []
    for px, py in raw_points:
        sx = int(round(px * scale + offset_x))

        sy = int(round(100 - (py * scale + offset_y)))
        sx = max(0, min(100, sx))
        sy = max(0, min(100, sy))
        result.append((sx, sy))

    return result


def calculate_triangle(side_a: str, side_b: str, side_c: str) -> tuple[str, Coordinates]:

    logging.debug(
        "Начало вычисления: side_a=%r, side_b=%r, side_c=%r",
        side_a, side_b, side_c
    )

    try:
        try:
            a = _parse_positive_float(side_a, "A")
            b = _parse_positive_float(side_b, "B")
            c = _parse_positive_float(side_c, "C")
        except ValueError as exc:
            logging.error(
                "Невалидные нечисловые данные: A=%r, B=%r, C=%r. Ошибка: %s",
                side_a, side_b, side_c, exc
            )
            return "", NON_NUMERIC_ERROR_COORDINATES.copy()
        except ArithmeticError as exc:
            logging.error(
                "Ошибочные числовые данные: A=%r, B=%r, C=%r. Ошибка: %s",
                side_a, side_b, side_c, exc
            )
            return "не треугольник", NUMERIC_ERROR_COORDINATES.copy()

        if a + b <= c or a + c <= b or b + c <= a:
            logging.warning(
                "Из заданных сторон нельзя построить треугольник: A=%s, B=%s, C=%s",
                a, b, c
            )
            return "не треугольник", NUMERIC_ERROR_COORDINATES.copy()

        triangle_type = _triangle_type(a, b, c)
        coordinates = _calculate_coordinates(a, b, c)

        logging.info(
            "Успешный запрос: параметры A=%s, B=%s, C=%s; результат: тип=%s, координаты=%s",
            a, b, c, triangle_type, coordinates
        )
        return triangle_type, coordinates

    except Exception:
        # Непредвиденный сбой логируется вместе с traceback.
        logging.exception(
            "Непредвиденная ошибка при запросе: A=%r, B=%r, C=%r",
            side_a, side_b, side_c
        )
        return "не треугольник", NUMERIC_ERROR_COORDINATES.copy()
