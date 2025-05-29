from os import walk
from os.path import splitext
from pathlib import Path


# true if file has .xml extension
def is_xml(file_name):
    return splitext(file_name)[1] == ".xml"


# Test data in the gitignored "private" subfolder or others will be used in
# addition to the test data committed to the repo
def get_test_data():
    data_files = [
        Path(dirpath) / name
        for dirpath, _, filenames in walk(Path(__file__).parent)
        for name in filenames
    ]
    for file in filter(is_xml, data_files):
        with open(file, "r") as f:
            yield f.read()
