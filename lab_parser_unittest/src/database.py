import sqlite3


class DatabaseRepository:
    MAX_NAME_LENGTH = 256
    MAX_MESSAGE_LENGTH = 8096

    def __init__(self, database_path: str):
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def _validate_id(self, comment_id: int):
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise TypeError("comment_id должен быть int")

    def _validate_username(self, username: str):
        if not isinstance(username, str):
            raise TypeError("username должен быть str")

        if not username:
            raise ValueError("username не может быть пустым")

        if len(username) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Длина username не должна превышать {self.MAX_NAME_LENGTH} символов"
            )

    def _validate_message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("message должен быть str")

        if not message:
            raise ValueError("message не может быть пустым")

        if len(message) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"Длина message не должна превышать {self.MAX_MESSAGE_LENGTH} символов"
            )

    def get_by_id(self, comment_id: int):
        self._validate_id(comment_id)

        cursor = self.connection.execute(
            """
            SELECT id, name, message
            FROM comments
            WHERE id = ?
            """,
            (comment_id,)
        )

        row = cursor.fetchone()
        if row is None:
            return None

        return dict(row)

    def get_by_name(self, username: str):
        self._validate_username(username)

        cursor = self.connection.execute(
            """
            SELECT id, name, message
            FROM comments
            WHERE name = ?
            ORDER BY id
            """,
            (username,)
        )

        return [dict(row) for row in cursor.fetchall()]

    def add(self, comment_id: int, username: str, message: str):
        self._validate_id(comment_id)
        self._validate_username(username)
        self._validate_message(message)

        self.connection.execute(
            """
            INSERT INTO comments (id, name, message)
            VALUES (?, ?, ?)
            """,
            (comment_id, username, message)
        )
        self.connection.commit()

        return True

    def update(self, comment_id: int, new_message: str):
        self._validate_id(comment_id)
        self._validate_message(new_message)

        cursor = self.connection.execute(
            """
            UPDATE comments
            SET message = ?
            WHERE id = ?
            """,
            (new_message, comment_id)
        )
        self.connection.commit()

        return cursor.rowcount > 0

    def delete(self, comment_id: int):
        self._validate_id(comment_id)

        cursor = self.connection.execute(
            """
            DELETE FROM comments
            WHERE id = ?
            """,
            (comment_id,)
        )
        self.connection.commit()

        return cursor.rowcount > 0

    def close(self):
        self.connection.close()
