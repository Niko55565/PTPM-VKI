from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from lab_parser_unittest.src.database import DatabaseRepository
from lab_parser_unittest.src.parser import ForumParser


class ForumParserTests(unittest.TestCase):

    def setUp(self):
        self.parser = ForumParser()

        self.repository = DatabaseRepository(":memory:")

        fixture_path = (
            Path(__file__).parent
            / "fixtures"
            / "forum_page.html"
        )

        self.html = fixture_path.read_text(
            encoding="utf-8"
        )

    def tearDown(self):
        self.repository.close()


    def test_parse_html_extracts_comments(self):
        data = self.parser.parse_html(self.html)

        self.assertEqual(
            len(data),
            2
        )

        self.assertEqual(
            data[0]["id"],
            1
        )

        self.assertEqual(
            data[0]["name"],
            "TestUser"
        )

        self.assertIn(
            "Первое тестовое сообщение",
            data[0]["message"]
        )

        self.assertEqual(
            data[1]["id"],
            2
        )

        self.assertEqual(
            data[1]["name"],
            "SecondUser"
        )


    def test_parse_html_skips_invalid_quote(self):
        html = """
        <div class="quote">
            <span class="text">
                Текст без автора
            </span>
        </div>
        """

        data = self.parser.parse_html(html)

        self.assertEqual(
            data,
            []
        )

    @patch("lab_parser_unittest.src.parser.requests.get")
    def test_parse_page_uses_requests_and_headers(
        self,
        mock_get
    ):
        response = Mock()

        response.text = self.html

        response.raise_for_status.return_value = None

        mock_get.return_value = response

        data = self.parser.parse_page(
            "https://quotes.toscrape.com/"
        )

        self.assertEqual(
            len(data),
            2
        )

        mock_get.assert_called_once_with(
            "https://quotes.toscrape.com/",
            headers=self.parser.HEADERS,
            timeout=10
        )

        response.raise_for_status.assert_called_once()


    def test_save_to_db_saves_parsed_data(self):
        data = self.parser.parse_html(
            self.html
        )

        saved_count = self.parser.save_to_db(
            data,
            self.repository
        )

        self.assertEqual(
            saved_count,
            2
        )

        first = self.repository.get_by_id(1)

        second = self.repository.get_by_id(2)

        self.assertEqual(
            first["name"],
            "TestUser"
        )

        self.assertEqual(
            second["name"],
            "SecondUser"
        )


if __name__ == "__main__":
    unittest.main()