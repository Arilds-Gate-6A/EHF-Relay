from requests import get
from typing import Iterable
 
from defusedxml.ElementTree import fromstring


def fetch_messages(auth: tuple[str, str], base_url: str = "https://ap-test.unit4.com/") -> Iterable[str]:
    inbox_response = get(base_url + "inbox", auth=auth)
    message_tree = fromstring(inbox_response.text)
    for message in message_tree.findall("./messages/message"):
        doc_link = message.find("xml-document").text
        doc_response = get(doc_link, auth=auth)
        yield doc_response.text
