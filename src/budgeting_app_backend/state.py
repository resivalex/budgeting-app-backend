from typing import List
from datetime import datetime

from budgeting_app_backend.protocols import SqlConnectionProtocol, SettingsProtocol

from .exporting import CsvExporting as TransactionsCsvExporting
from .importing import CsvImporting as TransactionsCsvImporting
from .transactions import (
    DbSource as TransactionsDbSource,
    Dump as TransactionsDump
)
from .settings import (
    SpendingLimits,
    SpendingLimitsValue
)
from budgeting_app_backend.settings.category_expansions import (
    CategoryExpansions,
    CategoryExpansionsValue
)


class State:

    def __init__(
            self,
            db_url: str,
            sql_connection: SqlConnectionProtocol,
            settings: SettingsProtocol
    ):
        self._db_url = db_url
        self._sql_connection = sql_connection
        self._settings = settings
        self._spending_limits = SpendingLimits(settings=settings)
        self._category_expansions = CategoryExpansions(settings=settings)

    def importing(self, content: bytes):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(csv_exporting.perform().encode('utf-8'))

        self._settings.set('transactions_uploaded_at', datetime.utcnow().isoformat())

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

    def dump(self):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)
        content = csv_exporting.perform().encode('utf-8')

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(content)

    def set_spending_limits(self, value: SpendingLimitsValue):
        self._spending_limits.set(value)

    def get_spending_limits(self):
        return self._spending_limits.get()

    def set_category_expansions(self, value: CategoryExpansionsValue):
        self._category_expansions.set(value)

    def get_category_expansions(self):
        return self._category_expansions.get()
