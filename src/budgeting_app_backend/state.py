from typing import List
from datetime import datetime

from budgeting_app_backend.protocols import SqlConnectionProtocol

from .exporting import CsvExporting as TransactionsCsvExporting
from .importing import CsvImporting as TransactionsCsvImporting
from .settings import Settings
from .transactions import (
    DbSource as TransactionsDbSource,
    Dump as TransactionsDump
)


class State:

    def __init__(self, db_url: str, sql_connection: SqlConnectionProtocol):
        self._db_url = db_url
        self._sql_connection = sql_connection

    def importing(self, content: bytes):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(csv_exporting.perform().encode('utf-8'))

        settings = Settings(sql_connection=self._sql_connection)
        settings.set('transactions_uploaded_at', datetime.utcnow().isoformat())

        csv_importing = TransactionsCsvImporting(url=self._db_url)
        csv_importing.perform(content)

    def exporting(self) -> bytes:
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        return csv_exporting.perform().encode('utf-8')

    def transactions(self) -> List:
        return TransactionsDbSource(url=self._db_url).all()

    def settings(self) -> dict:
        settings = Settings(sql_connection=self._sql_connection)

        return {
            'transactions_uploaded_at': settings.get('transactions_uploaded_at')
        }

    def dump(self):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)
        content = csv_exporting.perform().encode('utf-8')

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(content)
