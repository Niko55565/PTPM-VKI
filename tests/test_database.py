import sqlite3
import unittest

from lab_parser_unittest.src.database import DatabaseRepository


class DatabaseRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.repository = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repository.close()

    def test_add_success(self):
        result = self.repository.add(
            1,
            "kolya",
            "<p>Первое сообщение</p>"
        )

        self.assertTrue(result)

        comment = self.repository.get_by_id(1)

        self.assertEqual(comment["name"], "kolya")
        self.assertEqual(comment["message"], "<p>Первое сообщение</p>")

    def test_add_duplicate_id_raises_integrity_error(self):
        self.repository.add(
            1,
            "kolya",
            "<p>Первое сообщение</p>"
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add(
                1,
                "dima",
                "<p>Другое сообщение</p>"
            )

    def test_get_by_id_existing_comment(self):
        self.repository.add(
            10,
            "user1",
            "<b>Тест</b>"
        )

        comment = self.repository.get_by_id(10)

        self.assertEqual(comment["id"], 10)
        self.assertEqual(comment["name"], "user1")
        self.assertEqual(comment["message"], "<b>Тест</b>")

    def test_get_by_id_missing_comment_returns_none(self):
        comment = self.repository.get_by_id(999)

        self.assertIsNone(comment)

    def test_get_by_name_returns_all_user_comments(self):
        self.repository.add(1, "kolya", "<p>Один</p>")
        self.repository.add(2, "kolya", "<p>Два</p>")
        self.repository.add(3, "dima", "<p>Три</p>")

        comments = self.repository.get_by_name("kolya")

        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0]["id"], 1)
        self.assertEqual(comments[1]["id"], 2)

    def test_get_by_name_unknown_user_returns_empty_list(self):
        comments = self.repository.get_by_name("unknown")

        self.assertEqual(comments, [])

    def test_update_existing_comment(self):
        self.repository.add(
            5,
            "kolya",
            "<p>Старый текст</p>"
        )

        result = self.repository.update(
            5,
            "<p>Новый текст</p>"
        )

        self.assertTrue(result)

        comment = self.repository.get_by_id(5)

        self.assertEqual(
            comment["message"],
            "<p>Новый текст</p>"
        )

    def test_update_missing_comment_returns_false(self):
        result = self.repository.update(
            100,
            "<p>Новый текст</p>"
        )

        self.assertFalse(result)

    def test_delete_existing_comment(self):
        self.repository.add(
            7,
            "kolya",
            "<p>Удалить</p>"
        )

        result = self.repository.delete(7)

        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(7))

    def test_delete_missing_comment_returns_false(self):
        result = self.repository.delete(777)

        self.assertFalse(result)

    def test_add_too_long_username_raises_value_error(self):
        username = "a" * 257

        with self.assertRaises(ValueError):
            self.repository.add(
                20,
                username,
                "<p>Текст</p>"
            )

    def test_add_too_long_message_raises_value_error(self):
        message = "a" * 8097

        with self.assertRaises(ValueError):
            self.repository.add(
                21,
                "kolya",
                message
            )


if __name__ == "__main__":
    unittest.main()
