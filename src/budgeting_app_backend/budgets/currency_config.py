from pydantic import BaseModel
from typing import List

from budgeting_app_backend.protocols import SettingsProtocol


class ConversionRate(BaseModel):
    currency: str
    rate: float


class CurrencyConfigValue(BaseModel):
    main_currency: str
    conversion_rates: List[ConversionRate]


class CurrencyConfig:

    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> CurrencyConfigValue:
        return CurrencyConfigValue.parse_raw(self._settings.get('currency_config'))

    def set(self, value: CurrencyConfigValue):
        self._settings.set('currency_config', value.json())
