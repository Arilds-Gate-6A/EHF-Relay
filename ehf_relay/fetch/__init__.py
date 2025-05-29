from abc import ABC, abstractmethod
from typing import Iterable
 
class MessageFetcher(ABC):
    @abstractmethod
    def fetch(self) -> Iterable[str]:
        pass