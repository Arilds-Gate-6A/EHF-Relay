from requests import get, post
from typing import Iterable

from defusedxml.ElementTree import fromstring

from ehf_relay.config import REQUEST_TIMEOUT
from ehf_relay.fetch import MessageFetcher
from ehf_relay.model import EhfMessage


class Unit4Fetcher(MessageFetcher):
    def __init__(
        self, auth: tuple[str, str], base_url: str = "https://ap-test.unit4.com/"
    ):
        self.auth = auth
        self.base_url = base_url

    # Iterate messages from response XML
    def _read_message_page(self, message_tree: str) -> Iterable[EhfMessage]:
        for message in message_tree.findall("./messages/message"):
            doc_link = message.find("xml-document").text
            doc_response = get(doc_link, auth=self.auth, timeout=REQUEST_TIMEOUT)
            MessageFetcher._raise_if_error(doc_response)
            metadata = message.find("message_meta_data")
            yield EhfMessage(doc_response.text, metadata)

    def fetch(self) -> Iterable[EhfMessage]:
        message_tree = self._read_inbox()
        while True:  # Break when there is no "next" link
            yield from self._read_message_page(message_tree)
            link_next = message_tree.find("./navigation/next")
            if link_next is not None and link_next.text:
                message_tree = self._read_inbox(link_next.text)
            else:
                break

    def mark_read(self, message: EhfMessage):
        message_id = message.metadata.find("id").text
        post(
            self.base_url + f"inbox/{message_id}/read",
            auth=self.auth,
            timeout=REQUEST_TIMEOUT,
        )

    # Send GET and parse response, throwing exception on error
    def _read_inbox(self, url: str = None):
        url = url or self.base_url + "inbox"
        inbox_response = get(url, auth=self.auth, timeout=REQUEST_TIMEOUT)
        MessageFetcher._raise_if_error(inbox_response)
        Unit4Fetcher._raise_if_error(inbox_response)
        return fromstring(inbox_response.text)
