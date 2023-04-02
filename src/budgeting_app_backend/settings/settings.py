import sqlite3


SQLITE_PATH = 'data/budgeting-app.sqlite3'


class Settings:

    def __init__(self):
        self.__conn = sqlite3.connect(SQLITE_PATH)
        self.__conn.row_factory = sqlite3.Row
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()

    def get(self, name: str) -> str:
        self.__cursor.execute('''
            SELECT value
            FROM settings
            WHERE name = :name
        ''', {'name': name})
        row = self.__cursor.fetchone()
        return row['value'] if row else None

    def set(self, name: str, value: str) -> None:
        self.__cursor.execute('''
            INSERT OR REPLACE INTO settings
            (name, value)
            VALUES
            (:name, :value)
        ''', {'name': name, 'value': value})
