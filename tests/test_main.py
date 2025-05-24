from pathlib import Path
from unittest.mock import Mock

from sbdh_ubl_data.sbdh import StandardBusinessDocument

from ehf_relay import run

def mock_source():
    data_path = Path(__file__).parent / "data" / "example1.xml"
    with open(data_path, "r") as data_file:
        return [data_file.read()]

def test_run_main():
    mock_target = Mock()

    run(mock_source, mock_target)

    result = mock_target.call_args.args[0]
    assert type(result) is StandardBusinessDocument