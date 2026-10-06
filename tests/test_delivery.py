import unittest

from src.delivery import calculate_delivery_cost


class DeliveryTests(unittest.TestCase):
    def test_calculates_base_cost_for_regular_package(self):
        result = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-04"))

    def test_rejects_weight_below_minimum(self):
        result = calculate_delivery_cost(0.09, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_weight_above_maximum(self):
        result = calculate_delivery_cost(50.01, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_distance_below_minimum(self):
        result = calculate_delivery_cost(1, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_distance_above_maximum(self):
        result = calculate_delivery_cost(1, 5001, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_unknown_package_type(self):
        result = calculate_delivery_cost(1, 100, "неизвестный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_applies_medium_weight_coefficient(self):
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_applies_heavy_weight_coefficient(self):
        cost, _ = calculate_delivery_cost(20, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_adds_fragile_package_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_adds_dangerous_package_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_rounds_transport_days_up_for_partial_500_km(self):
        _, delivery_date = calculate_delivery_cost(1, 501, "обычный")
        self.assertEqual(delivery_date, "2026-09-05")

    def test_express_delivery_increases_cost(self):
        regular_cost, _ = calculate_delivery_cost(1, 100, "обычный", False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertGreater(express_cost, regular_cost)

    def test_express_delivery_takes_at_least_one_day(self):
        _, delivery_date = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertEqual(delivery_date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()
