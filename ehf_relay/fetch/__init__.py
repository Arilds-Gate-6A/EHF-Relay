from abc import ABC, abstractmethod
from typing import Iterable

from requests import Response

from ehf_relay.model import EhfMessage


class MessageFetcher(ABC):
    @abstractmethod
    def fetch(self) -> Iterable[EhfMessage]:
        pass

    @abstractmethod
    def mark_read(self, EhfMessage):
        pass

    # Raise an exception for HTTP errors
    @classmethod
    def _raise_if_error(cls, response: Response):
        if not response.status_code == 200:
            raise IOError(f"HTTP Error {response.status_code}: {response.reason}")
