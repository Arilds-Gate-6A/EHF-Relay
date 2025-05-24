from unittest.mock import Mock, patch

import ehf_relay

@patch("ehf_relay._parse")
def test_run_main(mock_parse):
    mock_parse.return_value = "parsed"

    mock_source = Mock()
    mock_source.return_value = ["A", "B", "C"]
    mock_target = Mock()
    mock_target.return_value = None

    ehf_relay.run(mock_source, mock_target)

    assert mock_target.call_args.args[0] == "parsed"