from typing import List
from datetime import datetime

from .exporting import CsvExporting as TransactionsCsvExporting
from .importing import CsvImporting as TransactionsCsvImporting
from .settings import Settings
from .transactions import (
    DbSource as TransactionsDbSource,
    Dump as TransactionsDump
)


class State:

    def __init__(self, db_url: str, sqlite_path: str):
        self._db_url = db_url
        self._sqlite_path = sqlite_path

    def importing(self, content: bytes):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        dump = TransactionsDump(sqlite_path=self._sqlite_path)
        dump.put(csv_exporting.perform().encode('utf-8'))

        settings = Settings(sqlite_path=self._sqlite_path)
        settings.set('transactions_uploaded_at', datetime.utcnow().isoformat())

        csv_importing = TransactionsCsvImporting(url=self._db_url)
        csv_importing.perform(content)

    def exporting(self) -> bytes:
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        return csv_exporting.perform().encode('utf-8')

    def transactions(self) -> List:
        return TransactionsDbSource(url=self._db_url).all()

    def settings(self) -> dict:
        settings = Settings(sqlite_path=self._sqlite_path)

        return {
            'transactions_uploaded_at': settings.get('transactions_uploaded_at')
        }

    def dump(self):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)
        content = csv_exporting.perform().encode('utf-8')

        dump = TransactionsDump(sqlite_path=self._sqlite_path)
        dump.put(content)
