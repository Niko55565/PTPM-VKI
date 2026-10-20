class TriangleCalculator:

    def calculate_triangle(self, side_a, side_b, side_c):
        try:
            a = float(side_a)
            b = float(side_b)
            c = float(side_c)
        except ValueError:
            return "", "Стороны должны быть числами"

        if (
            a <= 0
            or b <= 0
            or c <= 0
            or a + b <= c
            or a + c <= b
            or b + c <= a
        ):
            return "", "Треугольник не существует"

        unique_sides = len({a, b, c})

        triangle_type = {
            1: "равносторонний",
            2: "равнобедренный",
            3: "разносторонний"
        }[unique_sides]

        return triangle_type, ""