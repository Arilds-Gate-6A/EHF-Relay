from unittest.mock import Mock, patch

from requests import Response

from ehf_relay.fetch.unit4 import fetch_messages
from tests.data import read_data_file

def mock_response(text: str) -> Mock:
    mock_response = Mock(Response)
    mock_response.text = text
    return mock_response

# Should return the linked xml document for each message in the inbox
@patch("ehf_relay.fetch.unit4.get")
def test_read_messages(mock_get):
    auth = ("User", "Pass")
    responses = {
        "test/inbox": mock_response(read_data_file("unit4/inbox-response1.xml")),
        "https://ap-test.unit4.com/messages/4/xml-document": mock_response("Document 4"),
        "https://ap-test.unit4.com/messages/5/xml-document": mock_response("Document 5")
    }
    mock_get.side_effect = lambda path, auth: responses[path]

    result = list(fetch_messages(auth, "test/"))

    assert result == ["Document 4", "Document 5"]
        
# def test_read_paginated_messages():

# def test_mark_messages_read():

# def test_response_error():

# def test_get_message_error():
