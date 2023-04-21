from pydantic import BaseModel
from typing import List

from budgeting_app_backend.protocols import SettingsProtocol


class SpendingLimit(BaseModel):
    name: str
    currency: str
    amount: float
    categories: List[str]


class SpendingLimitsValue(BaseModel):
    limits: List[SpendingLimit]


class SpendingLimits:

    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> SpendingLimitsValue:
        return SpendingLimitsValue.parse_raw(self._settings.get('spending_limits'))

    def set(self, value: SpendingLimitsValue):
        self._settings.set('spending_limits', value.json())
