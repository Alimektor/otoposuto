import json
import os
from typing import Dict

from otoposuto.config import Config
from otoposuto.modules.base import Module
from otoposuto.utils import m_input, m_print, get_file_hash
from otoposuto.colors import red_color, green_color, blue_color, yellow_color


class PostedContent:
    def __init__(self, config: Config):
        self.config = config
        self.sent_post_file = os.path.expanduser(self.config.sent_post_file)
        self.source_folder = os.path.expanduser(self.config.source_folder)
        m_print(f"Use sent post file: {red_color}{self.sent_post_file}")
        m_print(f"Use source folder: {red_color}{self.source_folder}")

    def _get_file_hash(self, filename: str = None):
        return get_file_hash(os.path.join(self.source_folder, filename))

    def processing_markdown_files(self, modules: Dict[str, Module]):
        for markdown_file in os.listdir(self.source_folder):
            if not markdown_file.endswith(".md"):
                continue
            for module_name, module in modules.items():
                m_print(f"Processing module: {red_color}{module_name.upper()}")
                if self.processing_markdown_file(markdown_file, module, module_name):
                    m_print(f"Processed: {blue_color}{markdown_file}")
                else:
                    m_print(f"Failed to process: {red_color}{markdown_file}")

    def processing_markdown_file(self, markdown_file, module, module_name) -> bool:
        if self.is_posted(markdown_file, module_name):
            m_print(f"Already posted: {green_color}{markdown_file}")
            if self.is_changed(markdown_file, module_name):
                m_print(
                    f"Content changed for {blue_color}{markdown_file}{yellow_color}, processing..."
                )
                return self.change_markdown_file(markdown_file, module, module_name)
            return True
        m_print(
            f"Processing markdown file: {blue_color}{os.path.join(self.source_folder, markdown_file)}"
        )
        metadata = self.prompt_metadata(module_name, module)
        with open(
            os.path.join(self.source_folder, markdown_file), "r"
        ) as source_markdown_file:
            content = source_markdown_file.read()
        if self.just_mark(markdown_file, module_name):
            return True
        if module.post(content=content, metadata=metadata, filename=markdown_file):
            self.mark_as_posted(markdown_file, module_name, metadata)
        return True

    def just_mark(self, markdown_file, module_name) -> bool:
        to_mark = m_input(
            f"Just mark as posted for {blue_color}{markdown_file} {red_color}(yes/no) [no]: "
        )
        if to_mark == "yes":
            empty_metadata = {}
            self.mark_as_posted(markdown_file, module_name, empty_metadata)
            return True
        return False

    def change_markdown_file(self, markdown_file, module, module_name) -> bool:
        metadata = self.load_sent_posts()[markdown_file]["modules"][module_name][
            "metadata"
        ]
        with open(
            os.path.join(self.source_folder, markdown_file), "r"
        ) as source_markdown_file:
            content = source_markdown_file.read()
        if module.change(content, metadata, markdown_file):
            self.mark_as_posted(markdown_file, module_name, metadata)
        return True

    def load_sent_posts(self) -> Dict[str, list]:
        if not os.path.exists(self.sent_post_file):
            return {}
        with open(self.sent_post_file, "r") as f:
            return json.load(f)

    def save_sent_posts(self, data: Dict[str, list]):
        config_directory = os.path.dirname(self.sent_post_file)
        os.makedirs(config_directory, exist_ok=True)
        with open(self.sent_post_file, "w") as f:
            json.dump(data, f, indent=2)

    def is_posted(self, filename: str, module_name: str) -> bool:
        data = self.load_sent_posts()
        return module_name in data.get(filename, {}).get("modules", [])

    def is_changed(self, filename: str, module_name: str) -> bool:
        if self.check_hash(filename, module_name):
            return False
        m_print(
            f"Hash mismatch for {blue_color}{filename}{yellow_color}, repost processing"
        )
        return True

    def check_hash(self, filename: str, module_name: str) -> bool:
        data = self.load_sent_posts()
        return data.get(filename, {}).get("modules", {}).get(module_name, {}).get(
            "hash", ""
        ) == self._get_file_hash(filename)

    def mark_as_posted(self, filename: str, module_name: str, metadata: dict):
        data = self.load_sent_posts()
        if filename not in data:
            data[filename] = {}
        if module_name not in data[filename]:
            if "modules" not in data[filename]:
                data[filename]["modules"] = {}
            data[filename]["modules"].update(
                {
                    module_name: {
                        "hash": self._get_file_hash(filename),
                        "metadata": metadata,
                    }
                }
            )
            self.save_sent_posts(data)

    def prompt_metadata(self, module_name: str, module: Module) -> dict:
        module_config = self.config()["modules"][module_name]
        metadata = module.prompt_metadata(config=module_config)
        return metadata
