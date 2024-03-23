from pydantic import BaseModel
from typing import List
import copy

from budgeting_app_backend.protocols import SettingsProtocol


class MonthLimit(BaseModel):
    date: str
    currency: str
    amount: float


class SpendingLimit(BaseModel):
    name: str
    color: str
    categories: List[str]
    month_limits: List[MonthLimit]


class ConversionRate(BaseModel):
    currency: str
    rate: float


class CurrencyConfigValue(BaseModel):
    main_currency: str
    conversion_rates: List[ConversionRate]


class MonthCurrencyConfig(BaseModel):
    date: str
    config: CurrencyConfigValue


class SpendingLimitsValue(BaseModel):
    limits: List[SpendingLimit]
    month_currency_configs: List[MonthCurrencyConfig]


class MonthSliceSpendingLimit(BaseModel):
    name: str
    currency: str
    amount: float


class MonthSliceSpendingLimitsValue(BaseModel):
    date: str
    limits: List[MonthSliceSpendingLimit]
    currency_config: CurrencyConfigValue


class MonthItemSpendingLimitValue(BaseModel):
    date: str
    limit: MonthSliceSpendingLimit


class SpendingLimits:
    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> SpendingLimitsValue:
        return SpendingLimitsValue.parse_raw(self._settings.get("spending_limits"))

    def set(self, value: SpendingLimitsValue):
        self._settings.set("spending_limits", value.json())

    def get_month_budget(self, date: str) -> MonthSliceSpendingLimitsValue:
        value = self.get()

        currency_config = self._get_currency_config(value, date)
        limits = self._get_month_slice_limits(value, date)

        return MonthSliceSpendingLimitsValue(
            date=date,
            limits=limits,
            currency_config=currency_config,
        )

    def _get_currency_config(
        self, value: SpendingLimitsValue, date: str
    ) -> CurrencyConfigValue:
        for month_currency_config in value.month_currency_configs:
            if month_currency_config.date == date:
                return month_currency_config.config

        raise Exception(f"Currency config for {date} not found")

    def _get_month_slice_limits(
        self, value: SpendingLimitsValue, date: str
    ) -> List[MonthSliceSpendingLimit]:
        month_slice_limits = []
        for limit in value.limits:
            for month_limit in limit.month_limits:
                if month_limit.date == date:
                    month_slice_limit = MonthSliceSpendingLimit(
                        name=limit.name,
                        currency=month_limit.currency,
                        amount=month_limit.amount,
                    )
                    month_slice_limits.append(month_slice_limit)

        return month_slice_limits

    def set_month_budget(self, value: MonthSliceSpendingLimitsValue):
        updated_value = self.get()

        date = value.date
        updated_value = self._update_currency_config(
            updated_value, date, value.currency_config
        )
        updated_value = self._update_month_slice_limits(
            updated_value, date, value.limits
        )

        self.set(updated_value)

    def _update_currency_config(
        self,
        value: SpendingLimitsValue,
        date: str,
        currency_config: CurrencyConfigValue,
    ) -> SpendingLimitsValue:
        value = copy.deepcopy(value)
        for month_currency_config in value.month_currency_configs:
            if month_currency_config.date == date:
                month_currency_config.config = currency_config

                return value

        value.month_currency_configs.append(
            MonthCurrencyConfig(
                date=date,
                config=currency_config,
            )
        )

        return value

    def _update_month_slice_limits(
        self,
        value: SpendingLimitsValue,
        date: str,
        limits: List[MonthSliceSpendingLimit],
    ) -> SpendingLimitsValue:
        value = copy.deepcopy(value)
        current_limit_names = set([limit.name for limit in value.limits])
        new_limit_names = set([limit.name for limit in limits])

        if new_limit_names - current_limit_names:
            raise Exception(
                f"Unknown limit names: {new_limit_names - current_limit_names}"
            )

        for month_slice_limit in limits:
            for limit in value.limits:
                if limit.name == month_slice_limit.name:
                    date_found = False
                    for month_limit in limit.month_limits:
                        if month_limit.date == date:
                            month_limit.currency = month_slice_limit.currency
                            month_limit.amount = month_slice_limit.amount
                            date_found = True

                            break
                    if not date_found:
                        limit.month_limits.append(
                            MonthLimit(
                                date=date,
                                currency=month_slice_limit.currency,
                                amount=month_slice_limit.amount,
                            )
                        )

        return value

    def set_month_budget_item(self, value: MonthItemSpendingLimitValue):
        updated_value = self.get()

        date = value.date
        updated_value = self._update_month_slice_limits(
            updated_value, date, [value.limit]
        )

        self.set(updated_value)
