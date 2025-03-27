import argparse
import os
import importlib
import json
from typing import Dict
from otoposuto import posted_content
from otoposuto.config import Config
from otoposuto.modules.base import Module
from otoposuto.posted_content import PostedContent


def cli(config_path, use_modules: str = None):
    config = Config(config_path)
    posted_content = PostedContent(config)
    modules = config.get_modules(use_modules)
    posted_content.processing_markdown_files(modules)


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Post Markdown files to different posting systems."
        )
        parser.add_argument(
            "--config",
            "-c",
            type=str,
            default=os.path.expanduser("~/.config/otoposuto/config.yaml"),
            help="Path to the configuration file (Default: %(default)s)",
        )
        parser.add_argument(
            "--modules",
            "-m",
            type=str,
            help="Use modules.",
        )
        args = parser.parse_args()
        cli(args.config, args.modules)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
