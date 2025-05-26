from sbdh_ubl_data.sbdh.standard_business_document_header import (
    StandardBusinessDocument,
)
from sbdh_ubl_data.ubl.maindoc.ubl_credit_note_2_1 import CreditNote
from sbdh_ubl_data.ubl.maindoc.ubl_invoice_2_1 import Invoice

from ehf_relay import parse
from tests.util import get_test_data, parse_local_file

# example1.xml should parse correctly
def test_parse_example1():
    result = parse_local_file("example1.xml")

    assert type(result) is StandardBusinessDocument
    assert type(result.other_element) is Invoice


# Each test input file should produce a valid document
def test_parse_all():
    for data in get_test_data():
        result = parse(data)
        payload = result.other_element

        assert type(result) is StandardBusinessDocument
        assert type(payload) in [Invoice, CreditNote]
