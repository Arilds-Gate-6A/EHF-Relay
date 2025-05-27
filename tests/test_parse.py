from base64 import b64decode
from io import BytesIO

from pypdf import PdfReader
from sbdh_ubl_data.sbdh.standard_business_document_header import (
    StandardBusinessDocument,
)
from sbdh_ubl_data.ubl.maindoc.ubl_credit_note_2_1 import CreditNote
from sbdh_ubl_data.ubl.maindoc.ubl_invoice_2_1 import Invoice

from ehf_relay import parse
from tests.util import DATA_DIR, get_test_data, parse_local_file

# example1.xml should parse correctly
def test_parse_example1():
    result = parse_local_file("example1.xml")

    assert type(result) is StandardBusinessDocument
    assert type(result.other_element) is Invoice


def test_parse_example1_attachment():
    result = parse_local_file("example1.xml")
    doc_ref = result.other_element.additional_document_reference[0]
    attachment = doc_ref.attachment.embedded_document_binary_object

    reader = PdfReader(BytesIO(attachment.value))
    
    attachment_text = reader.pages[0].extract_text()
    assert attachment_text == "Example PDF attachment"


# Each test input file should produce a valid document
def test_parse_all():
    for data in get_test_data():
        result = parse(data)
        payload = result.other_element

        assert type(result) is StandardBusinessDocument
        assert type(payload) in [Invoice, CreditNote]


def test_read_pdf():
    with open(DATA_DIR / "Attachment1.pdf", "rb") as file:
        content = file.read()
    reader = PdfReader(BytesIO(content))
    text = reader.pages[0].extract_text()
    x = 3


def test_read_base64():
    with open(DATA_DIR / "Attachment1.txt") as file:
        text = file.read()
        data = b64decode(text)
    stream = BytesIO(data)
    reader = PdfReader(stream)
    text = reader.pages[0].extract_text()
    x = 3
