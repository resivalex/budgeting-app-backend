from typing import Protocol
from typing import Dict, List, Optional


class SqlConnectionProtocol(Protocol):
    def read(self, sql: str, params: Dict[str, str]) -> List[Dict]:
        ...

    def read_one(self, sql: str, params: Dict[str, str]) -> Optional[Dict]:
        ...

    def write(self, sql: str, params: Dict[str, str]) -> None:
        ...
