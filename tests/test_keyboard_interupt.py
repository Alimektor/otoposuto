# test_cli_app.py
import pytest
from unittest.mock import patch
from io import StringIO
from otoposuto.main import main
import sys


def test_keyboard_interrupt_handling(capsys):
    """
    Test that the CLI application handles KeyboardInterrupt gracefully.
    """
    test_args = ["otoposuto"]
    with patch.object(sys, "argv", test_args):
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            captured_output = StringIO()
            with patch("sys.stdout", new=captured_output):
                main()
        output = captured_output.getvalue().strip()
    assert "Exiting..." in output
