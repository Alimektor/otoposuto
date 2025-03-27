from io import StringIO
import sys
from unittest.mock import patch
import pytest

from otoposuto.main import main


@pytest.fixture()
def cli_app_fixture_with_system_exit():
    def _run_with_args_and_input(args, mock_input=None):
        test_args = ["otoposuto"] + args.split()
        with patch.object(sys, "argv", test_args):
            with patch("builtins.input", return_value=mock_input):
                captured_output = StringIO()
                with (
                    patch("sys.stdout", new=captured_output),
                    pytest.raises(SystemExit),
                ):
                    main()
        output = captured_output.getvalue().strip()
        return output

    yield _run_with_args_and_input


@pytest.mark.parametrize(
    "args, mock_input, expected_output",
    [
        ("--help", "", "Path to the configuration file"),
        ("-h", "", "Post Markdown files to different posting systems."),
    ],
)
def test_help(cli_app_fixture_with_system_exit, args, mock_input, expected_output):
    output = cli_app_fixture_with_system_exit(args, mock_input=mock_input)
    assert expected_output in output
