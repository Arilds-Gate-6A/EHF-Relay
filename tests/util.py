from os import walk
from os.path import splitext
from pathlib import Path

from ehf_relay import parse

DATA_DIR = Path(__file__).parent / "data"

# Test data in the gitignored "private" subfolder or others will be used in
# addition to the test data committed to the repo
def get_test_data():
    data_files = [
        Path(dirpath) / name
        for dirpath, _, filenames in walk(DATA_DIR)
        for name in filenames
    ]
    for file in filter(is_xml, data_files):
        with open(file, "r") as f:
            yield f.read()

# true if file has .xml extension
def is_xml(file_name):
    return splitext(file_name)[1] == ".xml"

# parse XML file in same dir
def parse_local_file(name):
    with open(DATA_DIR / "example1.xml", "r") as data_file:
        input_xml = data_file.read()
    return parse(input_xml)