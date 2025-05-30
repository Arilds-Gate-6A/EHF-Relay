from abc import ABC, abstractmethod
from typing import Iterable

from ehf_relay.model import EhfMessage
 
class MessageFetcher(ABC):
    @abstractmethod
    def fetch(self) -> Iterable[EhfMessage]:
        pass