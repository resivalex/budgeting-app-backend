from typing import Protocol


class SettingsProtocol(Protocol):
    def get(self, name: str) -> str:
        ...

    def set(self, name: str, value: str) -> None:
        ...
