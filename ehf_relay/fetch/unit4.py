from requests import get
from typing import Iterable

from defusedxml.ElementTree import fromstring

from ehf_relay.fetch import MessageFetcher


class Unit4Fetcher(MessageFetcher):
    def __init__(
        self, auth: tuple[str, str], base_url: str = "https://ap-test.unit4.com/"
    ):
        self.auth = auth
        self.base_url = base_url

    # Iterate messages from response XML
    def _read_message_page(self, message_tree: str) -> Iterable[str]:
        for message in message_tree.findall("./messages/message"):
            doc_link = message.find("xml-document").text
            doc_response = get(doc_link, auth=self.auth)
            yield doc_response.text

    def fetch(self) -> Iterable[str]:
        inbox_response = get(self.base_url + "inbox", auth=self.auth)
        message_tree = fromstring(inbox_response.text)
        while True:  # Break when there is no "next" link
            yield from self._read_message_page(message_tree)
            link_next = message_tree.find("./navigation/next")
            if link_next is not None and link_next.text:
                inbox_response = get(link_next.text, auth=self.auth)
                message_tree = fromstring(inbox_response.text)
            else:
                break
