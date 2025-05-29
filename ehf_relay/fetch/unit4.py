from requests import get
from typing import Iterable
 
from defusedxml.ElementTree import fromstring

from ehf_relay.fetch import MessageFetcher


class Unit4Fetcher(MessageFetcher):
    def __init__(self, auth: tuple[str, str], base_url: str = "https://ap-test.unit4.com/"):
        self.auth = auth
        self.base_url = base_url

    def fetch(self) -> Iterable[str]:
        inbox_response = get(self.base_url + "inbox", auth=self.auth)
        message_tree = fromstring(inbox_response.text)
        for message in message_tree.findall("./messages/message"):
            doc_link = message.find("xml-document").text
            doc_response = get(doc_link, auth=self.auth)
            yield doc_response.text
