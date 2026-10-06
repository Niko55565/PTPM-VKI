import math


NUMERIC_ERROR_COORDINATES = [(-1, -1), (-1, -1), (-1, -1)]
NON_NUMERIC_ERROR_COORDINATES = [(-2, -2), (-2, -2), (-2, -2)]


def _parse_positive_float(value, side_name):
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"Сторона {side_name} должна быть числом")

    if not math.isfinite(number) or number <= 0:
        raise ArithmeticError(f"Сторона {side_name} должна быть положительным конечным числом")

    return number


def _triangle_type(a, b, c):
    equal_ab = math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    equal_bc = math.isclose(b, c, rel_tol=1e-9, abs_tol=1e-12)
    equal_ac = math.isclose(a, c, rel_tol=1e-9, abs_tol=1e-12)

    if equal_ab and equal_bc:
        return "равносторонний"

    if equal_ab or equal_bc or equal_ac:
        return "равнобедренный"

    return "разносторонний"


def _calculate_coordinates(a, b, c):
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(b * b - x * x)

    points = [(0, 0), (c, 0), (x, y)]

    min_x = min(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)

    width = max_x - min_x
    height = max_y - min_y
    scale = 90 / max(width, height)

    result = []

    for px, py in points:
        sx = int((px - min_x) * scale) + 5
        sy = 95 - int((py - min_y) * scale)
        result.append((sx, sy))

    return result


def calculate_triangle(side_a, side_b, side_c):
    try:
        a = _parse_positive_float(side_a, "A")
        b = _parse_positive_float(side_b, "B")
        c = _parse_positive_float(side_c, "C")
    except ValueError:
        return "", NON_NUMERIC_ERROR_COORDINATES.copy()
    except ArithmeticError:
        return "не треугольник", NUMERIC_ERROR_COORDINATES.copy()

    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник", NUMERIC_ERROR_COORDINATES.copy()

    triangle_type = _triangle_type(a, b, c)
    coordinates = _calculate_coordinates(a, b, c)

    return triangle_type, coordinates
