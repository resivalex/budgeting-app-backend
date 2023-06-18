from pydantic import BaseModel
import datetime

from budgeting_app_backend.protocols import SettingsProtocol


class UploadDetailsValue(BaseModel):
    transactions_uploaded_at: str


class UploadDetails:
    def __init__(self, settings: SettingsProtocol):
        self._settings = settings

    def get(self) -> UploadDetailsValue:
        setting_value = self._settings.get("transactions_uploaded_at")

        if setting_value is None:
            return UploadDetailsValue(
                transactions_uploaded_at=datetime.datetime(1970, 1, 1).isoformat()
            )

        return UploadDetailsValue(transactions_uploaded_at=setting_value)

    def set(self, uploaded_at: str):
        self._settings.set("transactions_uploaded_at", uploaded_at)
