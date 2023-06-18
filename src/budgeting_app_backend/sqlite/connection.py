import sqlite3
from typing import Dict, List, Optional


class Connection:
    def __init__(self, sqlite_path: str):
        self.__conn = sqlite3.connect(sqlite_path)
        self.__conn.row_factory = sqlite3.Row
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()

    def read(self, sql: str, params: Dict[str, str]) -> List[Dict]:
        self.__cursor.execute(sql, params)
        rows = self.__cursor.fetchall()

        return [dict(row) for row in rows]

    def read_one(self, sql: str, params: Dict[str, str]) -> Optional[Dict]:
        self.__cursor.execute(sql, params)
        row = self.__cursor.fetchone()

        return dict(row) if row else None

    def write(self, sql: str, params: Dict[str, str]) -> None:
        self.__cursor.execute(sql, params)
        self.__conn.commit()
