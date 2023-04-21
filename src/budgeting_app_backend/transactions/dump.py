from datetime import datetime

from budgeting_app_backend.protocols import SqlConnectionProtocol


class Dump:

    def __init__(self, sql_connection: SqlConnectionProtocol):
        self._sql_connection = sql_connection

    def put(self, content: str) -> None:
        uploaded_at = datetime.utcnow().isoformat()

        self._sql_connection.write('''
            INSERT INTO dumps
            (uploaded_at, content)
            VALUES
            (:uploaded_at, :content)
        ''', {'uploaded_at': uploaded_at, 'content': content})
