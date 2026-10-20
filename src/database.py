import sqlite3


class TriangleDatabase:

    def __init__(self, database_name="triangles.db"):
        self.connection = sqlite3.connect(database_name)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT,
                side_b TEXT,
                side_c TEXT,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)

        self.connection.commit()

    def add(self, side_a, side_b, side_c, triangle_type, error_message):
        self.connection.execute(
            """
            INSERT INTO triangles
            (side_a, side_b, side_c, triangle_type, error_message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                side_a,
                side_b,
                side_c,
                triangle_type,
                error_message
            )
        )

        self.connection.commit()

    def get(self, side_a, side_b, side_c):
        cursor = self.connection.execute(
            """
            SELECT side_a, side_b, side_c, triangle_type, error_message
            FROM triangles
            WHERE side_a = ?
              AND side_b = ?
              AND side_c = ?
            """,
            (
                side_a,
                side_b,
                side_c
            )
        )

        return cursor.fetchone()

    def delete(self, side_a, side_b, side_c):
        self.connection.execute(
            """
            DELETE FROM triangles
            WHERE side_a = ?
              AND side_b = ?
              AND side_c = ?
            """,
            (
                side_a,
                side_b,
                side_c
            )
        )

        self.connection.commit()