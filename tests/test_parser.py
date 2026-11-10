from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from src.database import DatabaseRepository
from src.parser import ForumParser


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
        comments = self.parser.parse_html(self.html)

        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0]["id"], 101)
        self.assertEqual(comments[0]["name"], "TestUser")
        self.assertIn(
            "Первое тестовое сообщение",
            comments[0]["message"]
        )
        self.assertEqual(comments[1]["id"], 102)
        self.assertEqual(comments[1]["name"], "SecondUser")

    def test_parse_html_skips_invalid_comment(self):
        html = """
        <html>
            <body>
                <div class="comment" data-comment-id="abc">
                    <span class="author">User</span>
                    <div class="message">Текст</div>
                </div>
            </body>
        </html>
        """

        comments = self.parser.parse_html(html)

        self.assertEqual(comments, [])

    @patch("src.parser.requests.get")
    def test_parse_page_uses_requests_and_headers(self, mock_get):
        response = Mock()
        response.text = self.html
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        comments = self.parser.parse_page(
            "https://example.com/forum"
        )

        self.assertEqual(len(comments), 2)

        mock_get.assert_called_once_with(
            "https://example.com/forum",
            headers=self.parser.HEADERS,
            timeout=10
        )

        response.raise_for_status.assert_called_once()

    def test_save_to_db_saves_parsed_comments(self):
        comments = self.parser.parse_html(self.html)

        saved_count = self.parser.save_to_db(
            comments,
            self.repository
        )

        self.assertEqual(saved_count, 2)

        first_comment = self.repository.get_by_id(101)
        second_comment = self.repository.get_by_id(102)

        self.assertEqual(first_comment["name"], "TestUser")
        self.assertEqual(second_comment["name"], "SecondUser")


if __name__ == "__main__":
    unittest.main()
