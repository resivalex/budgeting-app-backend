from typing import List
from datetime import datetime

from budgeting_app_backend.protocols import SqlConnectionProtocol, SettingsProtocol

from .exporting import CsvExporting as TransactionsCsvExporting
from .importing import CsvImporting as TransactionsCsvImporting
from .transactions import DbSource as TransactionsDbSource, Dump as TransactionsDump
from .settings import (
    SpendingLimits,
    SpendingLimitsValue,
    MonthSliceSpendingLimitsValue,
    MonthItemSpendingLimitValue,
    CategoryExpansions,
    CategoryExpansionsValue,
    AccountProperties,
    AccountPropertiesValue,
    UploadDetails,
    UploadDetailsValue,
)


class State:
    def __init__(
        self,
        db_url: str,
        sql_connection: SqlConnectionProtocol,
        settings: SettingsProtocol,
    ):
        self._db_url = db_url
        self._sql_connection = sql_connection
        self._spending_limits = SpendingLimits(settings=settings)
        self._category_expansions = CategoryExpansions(settings=settings)
        self._account_properties = AccountProperties(settings=settings)
        self._upload_details = UploadDetails(settings=settings)

    def importing(self, content: bytes):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(csv_exporting.perform().encode("utf-8"))

        self._upload_details.set(uploaded_at=datetime.utcnow().isoformat())

        csv_importing = TransactionsCsvImporting(url=self._db_url)
        csv_importing.perform(content)

    def exporting(self) -> bytes:
        csv_exporting = TransactionsCsvExporting(url=self._db_url)

        return csv_exporting.perform().encode("utf-8")

    def transactions(self) -> List:
        return TransactionsDbSource(url=self._db_url).all()

    def settings(self) -> UploadDetailsValue:
        return self._upload_details.get()

    def dump(self):
        csv_exporting = TransactionsCsvExporting(url=self._db_url)
        content = csv_exporting.perform().encode("utf-8")

        dump = TransactionsDump(sql_connection=self._sql_connection)
        dump.put(content)

    def set_spending_limits(self, value: SpendingLimitsValue):
        self._spending_limits.set(value)

    def get_spending_limits(self):
        return self._spending_limits.get()

    def set_budget_month_limit(self, value: MonthSliceSpendingLimitsValue):
        self._spending_limits.set_month_budget(value)

    def get_budget_month_limit(self, month: str) -> MonthSliceSpendingLimitsValue:
        return self._spending_limits.get_month_budget(month)

    def set_budget_month_item_limit(self, value: MonthItemSpendingLimitValue):
        self._spending_limits.set_month_budget_item(value)

    def set_category_expansions(self, value: CategoryExpansionsValue):
        self._category_expansions.set(value)

    def get_category_expansions(self):
        return self._category_expansions.get()

    def set_account_properties(self, value: AccountPropertiesValue):
        self._account_properties.set(value)

    def get_account_properties(self):
        return self._account_properties.get()
