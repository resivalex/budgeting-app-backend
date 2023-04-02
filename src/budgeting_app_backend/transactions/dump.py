import sqlite3
from datetime import datetime


class Dump:

    def __init__(self, sqlite_path: str):
        self.__conn = sqlite3.connect(sqlite_path)
        self.__conn.row_factory = sqlite3.Row
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()

    def put(self, content: str) -> None:
        uploaded_at = datetime.now().isoformat()

        self.__cursor.execute('''
            INSERT INTO dumps
            (uploaded_at, content)
            VALUES
            (:uploaded_at, :content)
        ''', {'uploaded_at': uploaded_at, 'content': content})
        self.__conn.commit()
