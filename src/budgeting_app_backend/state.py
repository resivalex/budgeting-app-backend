from typing import List

from .exporting import CsvExporting as TransactionsCsvExporting
from .importing import CsvImporting as TransactionsCsvImporting
from .settings import Settings
from .transactions import DbSource as TransactionsDbSource


class State:

    def __init__(self, db_url: str, sqlite_path: str):
        self._db_url = db_url
        self._settings = Settings(sqlite_path=sqlite_path)

    def importing(self, content: bytes):
        csv_importing = TransactionsCsvImporting(url=self._db_url)
        csv_importing.perform(content)

    def exporting(self) -> bytes:
        csv_exporting = TransactionsCsvExporting(url=self._db_url)
        return csv_exporting.perform().encode('utf-8')

    def transactions(self) -> List:
        return TransactionsDbSource(url=self._db_url).all()

    def settings(self) -> dict:
        return {
            'transactions_uploaded_at': self._settings.get('transactions_uploaded_at')
        }
