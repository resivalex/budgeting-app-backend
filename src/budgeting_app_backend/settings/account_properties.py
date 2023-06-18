from pydantic import BaseModel
from typing import List

from budgeting_app_backend.protocols import SettingsProtocol


class SingleAccountProperties(BaseModel):
    name: str
    color: str


class AccountPropertiesValue(BaseModel):
    accounts: List[SingleAccountProperties]


class AccountProperties:
    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> AccountPropertiesValue:
        setting_value = self._settings.get("account_properties")

        if setting_value is None:
            return AccountPropertiesValue(accounts=[])

        return AccountPropertiesValue.parse_raw(setting_value)

    def set(self, value: AccountPropertiesValue):
        self._settings.set("account_properties", value.json())
