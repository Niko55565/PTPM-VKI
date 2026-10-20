import unittest
from unittest.mock import Mock, patch

from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.user_interface import UserInterface, ConsoleUserInterface
from src.external_service import ExternalService, ServerService
from src.controller import Controller


class Lab3Tests(unittest.TestCase):

    def setUp(self):
        self.database = TriangleDatabase(":memory:")

    def tearDown(self):
        self.database.connection.close()

    def test_integration_new_triangle_is_calculated_saved_and_sent(self):
        calculator = TriangleCalculator()

        user_interface = Mock(spec=UserInterface)
        user_interface.get_data.return_value = ("3", "4", "5")

        external_service = Mock(spec=ExternalService)

        controller = Controller(
            calculator,
            self.database,
            user_interface,
            external_service
        )

        result = controller.run()

        self.assertEqual(result, "разносторонний")

        record = self.database.get("3", "4", "5")

        self.assertIsNotNone(record)
        self.assertEqual(record[3], "разносторонний")
        self.assertEqual(record[4], "")

        external_service.send.assert_called_once_with(
            "разносторонний"
        )

        self.database.delete("3", "4", "5")

        self.assertIsNone(
            self.database.get("3", "4", "5")
        )

    def test_integration_existing_triangle_is_taken_from_database(self):
        self.database.add(
            "5",
            "5",
            "5",
            "равносторонний",
            ""
        )

        calculator = Mock(spec=TriangleCalculator)

        user_interface = Mock(spec=UserInterface)
        user_interface.get_data.return_value = ("5", "5", "5")

        external_service = Mock(spec=ExternalService)

        controller = Controller(
            calculator,
            self.database,
            user_interface,
            external_service
        )

        result = controller.run()

        self.assertEqual(result, "равносторонний")

        calculator.calculate_triangle.assert_not_called()

        external_service.send.assert_called_once_with(
            "равносторонний"
        )

    def test_integration_invalid_triangle_is_saved_as_error(self):
        calculator = TriangleCalculator()

        user_interface = Mock(spec=UserInterface)
        user_interface.get_data.return_value = ("1", "2", "3")

        external_service = Mock(spec=ExternalService)

        controller = Controller(
            calculator,
            self.database,
            user_interface,
            external_service
        )

        result = controller.run()

        self.assertEqual(
            result,
            "Треугольник не существует"
        )

        record = self.database.get("1", "2", "3")

        self.assertIsNotNone(record)

        self.assertEqual(
            record[4],
            "Треугольник не существует"
        )

        external_service.send.assert_called_once_with(
            "Треугольник не существует"
        )

    def test_integration_non_numeric_input_is_saved_as_error(self):
        calculator = TriangleCalculator()

        user_interface = Mock(spec=UserInterface)
        user_interface.get_data.return_value = (
            "abc",
            "4",
            "5"
        )

        external_service = Mock(spec=ExternalService)

        controller = Controller(
            calculator,
            self.database,
            user_interface,
            external_service
        )

        result = controller.run()

        self.assertEqual(
            result,
            "Стороны должны быть числами"
        )

        record = self.database.get(
            "abc",
            "4",
            "5"
        )

        self.assertIsNotNone(record)

        self.assertEqual(
            record[4],
            "Стороны должны быть числами"
        )

    @patch(
        "builtins.input",
        side_effect=["3", "4", "5"]
    )
    def test_user_input_with_patch(self, mock_input):
        user_interface = ConsoleUserInterface()

        result = user_interface.get_data()

        self.assertEqual(
            result,
            ("3", "4", "5")
        )

        self.assertEqual(
            mock_input.call_count,
            3
        )

    @patch("builtins.print")
    def test_external_service_send_with_patch(self, mock_print):
        service = ServerService()

        service.send("разносторонний")

        mock_print.assert_called_once_with(
            "Отправка на внешний сервер: разносторонний"
        )


if __name__ == "__main__":
    unittest.main()