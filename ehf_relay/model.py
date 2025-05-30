from dataclasses import dataclass
from typing import Any


@dataclass
class EhfMessage:
    raw_xml: str
    metadata: Any
