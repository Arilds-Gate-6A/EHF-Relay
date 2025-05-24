from os import walk
from os.path import splitext
from pathlib import Path

from sbdh_ubl_data.sbdh.standard_business_document_header import StandardBusinessDocument

from ehf_relay import parse

DATA_DIR = Path(__file__).parent / "data"

# true if file has .xml extension
def _is_xml(file_name):
    return splitext(file_name)[1] == ".xml"

# example1.xml should parse correctly
def test_parse_example1():
    with open(DATA_DIR / "example1.xml", "r") as data_file:
        input_xml = data_file.read()
    result = parse(input_xml)
    assert type(result) is StandardBusinessDocument

# Test data in the gitignored "private" subfolder or others will be used in
# addition to the test data committed to the repo
def get_test_data():
    data_files = [Path(dirpath) / name for dirpath, _, filenames in walk(DATA_DIR) for name in filenames]
    for file in filter(_is_xml, data_files):
        with open(file, "r") as f:
            yield f.read()

# Each test input file should produce a valid document
def test_parse_all():
    for data in get_test_data():
        result = parse(data)
        assert type(result) is StandardBusinessDocument