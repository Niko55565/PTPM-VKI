import math
import unittest

from triangle import (
    NON_NUMERIC_ERROR_COORDINATES,
    NUMERIC_ERROR_COORDINATES,
    calculate_triangle,
)


class TriangleTests(unittest.TestCase):
    def assert_coordinates_valid(self, coordinates):
        self.assertEqual(len(coordinates), 3)
        for x, y in coordinates:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_equilateral(self):
        triangle_type, coordinates = calculate_triangle("5", "5", "5")
        self.assertEqual(triangle_type, "равносторонний")
        self.assert_coordinates_valid(coordinates)

    def test_isosceles(self):
        triangle_type, coordinates = calculate_triangle("5", "5", "8")
        self.assertEqual(triangle_type, "равнобедренный")
        self.assert_coordinates_valid(coordinates)

    def test_scalene(self):
        triangle_type, coordinates = calculate_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")
        self.assert_coordinates_valid(coordinates)

    def test_triangle_inequality(self):
        triangle_type, coordinates = calculate_triangle("1", "2", "3")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_negative_number(self):
        triangle_type, coordinates = calculate_triangle("-1", "2", "2")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_zero(self):
        triangle_type, coordinates = calculate_triangle("0", "2", "2")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_nan(self):
        triangle_type, coordinates = calculate_triangle("nan", "2", "2")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_infinity(self):
        triangle_type, coordinates = calculate_triangle("inf", "2", "2")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coordinates, NUMERIC_ERROR_COORDINATES)

    def test_non_numeric(self):
        triangle_type, coordinates = calculate_triangle("abc", "2", "2")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coordinates, NON_NUMERIC_ERROR_COORDINATES)

    def test_float_values(self):
        triangle_type, coordinates = calculate_triangle("2.5", "3.5", "4.5")
        self.assertEqual(triangle_type, "разносторонний")
        self.assert_coordinates_valid(coordinates)


if __name__ == "__main__":
    unittest.main()
