from unittest.mock import Mock, patch

from pytest import raises
from requests import Response

from ehf_relay.fetch.unit4 import Unit4Fetcher
from ehf_relay.model import EhfMessage
from tests.data import read_data_file

AUTH = ("User", "Pass")


def mock_response(text: str) -> Mock:
    mock_response = Mock(Response)
    mock_response.status_code = 200
    mock_response.text = text
    return mock_response


# Should return the linked xml document for each message in the inbox
@patch("ehf_relay.fetch.unit4.get")
def test_read_messages(mock_get: Mock):
    responses = {
        "test/inbox": mock_response(read_data_file("unit4/inbox-response1.xml")),
        "https://ap-test.unit4.com/messages/4/xml-document": mock_response(
            "Document 4"
        ),
        "https://ap-test.unit4.com/messages/5/xml-document": mock_response(
            "Document 5"
        ),
    }
    mock_get.side_effect = lambda path, auth: responses[path]
    fetcher = Unit4Fetcher(AUTH, "test/")

    result = [item.raw_xml for item in fetcher.fetch()]

    assert result == ["Document 4", "Document 5"]


# Reads paginated inbox results
@patch("ehf_relay.fetch.unit4.get")
def test_read_paginated_messages(mock_get: Mock):
    responses = {
        "test/inbox": mock_response(read_data_file("unit4/inbox-response2-1.xml")),
        "https://ap-test.unit4.com/messages?index=6": mock_response(
            read_data_file("unit4/inbox-response2-2.xml")
        ),
        "https://ap-test.unit4.com/messages?index=7": mock_response(
            read_data_file("unit4/inbox-response2-3.xml")
        ),
        "https://ap-test.unit4.com/messages/4/xml-document": mock_response(
            "Document 4"
        ),
        "https://ap-test.unit4.com/messages/5/xml-document": mock_response(
            "Document 5"
        ),
        "https://ap-test.unit4.com/messages/6/xml-document": mock_response(
            "Document 6"
        ),
        "https://ap-test.unit4.com/messages/7/xml-document": mock_response(
            "Document 7"
        ),
        "https://ap-test.unit4.com/messages/8/xml-document": mock_response(
            "Document 8"
        ),
    }
    mock_get.side_effect = lambda path, auth: responses[path]
    fetcher = Unit4Fetcher(AUTH, "test/")

    result = [item.raw_xml for item in fetcher.fetch()]

    assert result == [f"Document {n}" for n in range(4, 9)]


@patch("ehf_relay.fetch.unit4.post")
def test_mark_messages_read(mock_post: Mock):
    fetcher = Unit4Fetcher(AUTH, "test/")
    mock_id = Mock()
    mock_id.text = "20"
    mock_meta = Mock()
    mock_meta.find.return_value = mock_id
    message = EhfMessage("xml", mock_meta)

    fetcher.mark_read(message)

    mock_post.assert_called_once_with("test/inbox/20/read")


# Raise exception if inbox GET fails
@patch("ehf_relay.fetch.unit4.get")
def test_bad_request(mock_get: Mock):
    bad_request = Mock(Response)
    bad_request.reason = "Bad request"
    bad_request.status_code = 400
    responses = {
        "test/inbox": bad_request,
        "https://ap-test.unit4.com/messages/4/xml-document": mock_response(
            "Document 4"
        ),
        "https://ap-test.unit4.com/messages/5/xml-document": mock_response(
            "Document 5"
        ),
    }
    mock_get.side_effect = lambda path, auth: responses[path]
    fetcher = Unit4Fetcher(AUTH, "test/")

    with raises(IOError, match="HTTP Error 400: Bad request"):
        list(fetcher.fetch())


@patch("ehf_relay.fetch.unit4.get")
def test_not_found(mock_get: Mock):
    not_found = Mock(Response)
    not_found.reason = "Not found"
    not_found.status_code = 404
    responses = {
        "test/inbox": mock_response(read_data_file("unit4/inbox-response1.xml")),
        "https://ap-test.unit4.com/messages/4/xml-document": not_found,
        "https://ap-test.unit4.com/messages/5/xml-document": mock_response(
            "Document 5"
        ),
    }
    mock_get.side_effect = lambda path, auth: responses[path]
    fetcher = Unit4Fetcher(AUTH, "test/")

    with raises(IOError, match="HTTP Error 404: Not found"):
        list(fetcher.fetch())

# def test_get_message_error():
