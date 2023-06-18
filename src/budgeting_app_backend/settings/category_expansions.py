from pydantic import BaseModel
from typing import List

from budgeting_app_backend.protocols import SettingsProtocol


class CategoryExpansion(BaseModel):
    name: str
    expandedName: str


class CategoryExpansionsValue(BaseModel):
    expansions: List[CategoryExpansion]


class CategoryExpansions:
    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> CategoryExpansionsValue:
        setting_value = self._settings.get("category_expansions")

        if setting_value is None:
            return CategoryExpansionsValue(categoryExpansions=[])

        return CategoryExpansionsValue.parse_raw(setting_value)

    def set(self, value: CategoryExpansionsValue):
        self._settings.set("category_expansions", value.json())
