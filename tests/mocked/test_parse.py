from io import BytesIO

from pypdf import PdfReader
from sbdh_ubl_data.sbdh.standard_business_document_header import (
    StandardBusinessDocument,
)
from sbdh_ubl_data.ubl.maindoc.ubl_credit_note_2_1 import CreditNote
from sbdh_ubl_data.ubl.maindoc.ubl_invoice_2_1 import Invoice

from ehf_relay import parse
from tests.data import read_data_file
from tests.data.ehf import get_test_data


# example1.xml should parse correctly
def test_parse_example1():
    result = parse(read_data_file("ehf/example1.xml"))

    assert type(result) is StandardBusinessDocument
    assert type(result.other_element) is Invoice


# base64 attachment in xml is converted to bytes
def test_parse_example1_attachment():
    result = parse(read_data_file("ehf/example1.xml"))
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
