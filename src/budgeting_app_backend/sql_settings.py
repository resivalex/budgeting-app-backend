from budgeting_app_backend.protocols import SqlConnectionProtocol


class SqlSettings:
    def __init__(self, sql_connection: SqlConnectionProtocol):
        self._sql_connection = sql_connection

    def get(self, name: str) -> str:
        row = self._sql_connection.read_one(
            """
            SELECT value
            FROM settings
            WHERE name = :name
        """,
            {"name": name},
        )

        return row["value"] if row else None

    def set(self, name: str, value: str) -> None:
        self._sql_connection.write(
            """
            INSERT OR REPLACE INTO settings
            (name, value)
            VALUES
            (:name, :value)
        """,
            {"name": name, "value": value},
        )
