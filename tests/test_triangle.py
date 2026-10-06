import unittest

from src.triangle import (
    NON_NUMERIC_ERROR_COORDINATES,
    NUMERIC_ERROR_COORDINATES,
    calculate_triangle,
)


class TriangleTests(unittest.TestCase):
    def test_returns_equilateral_triangle(self):
        triangle_type, _ = calculate_triangle("5", "5", "5")
        self.assertEqual(triangle_type, "равносторонний")

    def test_returns_isosceles_triangle(self):
        triangle_type, _ = calculate_triangle("5", "5", "8")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_returns_scalene_triangle(self):
        triangle_type, _ = calculate_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_rejects_non_numeric_side(self):
        triangle_type, coordinates = calculate_triangle("abc", "4", "5")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coordinates, NON_NUMERIC_ERROR_COORDINATES)

    def test_rejects_zero_side(self):
        triangle_type, coordinates = calculate_triangle("0", "4", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_rejects_negative_side(self):
        triangle_type, coordinates = calculate_triangle("-1", "4", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_rejects_nan_side(self):
        triangle_type, coordinates = calculate_triangle("nan", "4", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_rejects_broken_triangle_inequality(self):
        triangle_type, coordinates = calculate_triangle("1", "2", "3")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_accepts_fractional_sides(self):
        triangle_type, _ = calculate_triangle("2.5", "3.5", "4.5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_returns_three_integer_coordinates_inside_field(self):
        _, coordinates = calculate_triangle("3", "4", "5")

        self.assertEqual(len(coordinates), 3)
        for x, y in coordinates:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)


if __name__ == "__main__":
    unittest.main()
