from io import StringIO
import os
import shutil
import sys
import pytest
from unittest.mock import patch

import yaml
import otoposuto
from otoposuto.main import main


@pytest.fixture()
def cli_app_fixture(capsys, tmp_path):
    config_path = f"{tmp_path}/.test-otoposuto/config.yaml"
    os.makedirs(f"{tmp_path}/.test-otoposuto/posts", exist_ok=True)
    if not os.path.exists(config_path):
        default_config = {
            "source": f"{tmp_path}/.test-otoposuto/posts",
            "sent_post_file": f"{tmp_path}/.test-otoposuto/sent_posts.json",
            "modules": {"dumb": {"metadata": {"title": "", "description": ""}}},
        }
        with open(config_path, "w") as f:
            yaml.dump(default_config, f)

    def _run_with_args_and_input(args, mock_input=None):
        test_args = ["otoposuto"] + args.split()
        with patch.object(sys, "argv", test_args):
            with patch("builtins.input", return_value=mock_input):
                captured_output = StringIO()
                with patch("sys.stdout", new=captured_output):
                    main()
        output = captured_output.getvalue().strip()
        return output

    yield _run_with_args_and_input
    # Remove testing files
    shutil.rmtree(f"{tmp_path}/.test-otoposuto")


@pytest.fixture()
def markdown_file(tmp_path):
    with open(
        os.path.expanduser(f"{tmp_path}/.test-otoposuto/posts/test.md"), "w+"
    ) as markdown_file:
        markdown_file.write("# Test Title\n\nTest Description")
