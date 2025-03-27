import importlib
from typing import Dict
import yaml
import os
from otoposuto.modules.base import Module
from otoposuto.utils import m_print
from otoposuto.colors import red_color, reset_color, yellow_color


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to ensure only one instance is created.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._settings = {}
        return cls._instance

    def __init__(self, config_path: str):
        self.config_path = config_path
        m_print(f"Use config file: {red_color}{self.path}")
        source_folder = os.path.expanduser(self()["source"])
        if not source_folder:
            raise Exception(f"No source folder specified in {self.path}")
        if not os.path.exists(source_folder):
            raise Exception(f"Source folder {source_folder} does not exist")

    @property
    def path(self):
        return self.config_path

    @property
    def source_folder(self):
        return os.path.expanduser(self()["source"])

    @property
    def sent_post_file(self):
        return os.path.expanduser(self()["sent_post_file"])

    def __call__(self, *args, **kwargs):
        # Get directory for path
        config_directory = os.path.dirname(os.path.expanduser(self.config_path))
        os.makedirs(config_directory, exist_ok=True)
        if not os.path.exists(self.config_path):
            default_config = {
                "source": input("Source folder for Markdown files: "),
                "sent_post_file": "~/.config/otoposuto/sent_posts.json",
                "modules": {"dumb": {"metadata": {"title": "", "description": ""}}},
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default_config, f)
        return yaml.safe_load(open(self.config_path))

    def get_modules(self, use_modules: str = None) -> Dict[str, Module]:
        all_modules_in_config = list(self()["modules"].keys())
        if not use_modules:
            modules_input = input(
                f"Enter modules to use (Space-separated. Default: all modules in config: {red_color}{all_modules_in_config}{reset_color}): "
            ).strip()
        else:
            m_print(
                f"Use modules from command line: {red_color}{use_modules}{reset_color}"
            )
            modules_input = use_modules
        if not modules_input:
            modules_input = " ".join(all_modules_in_config)

        modules = modules_input.split() if modules_input else ["dumb"]
        modules = self.load_modules(modules)
        return modules

    def load_modules(self, modules: list) -> Dict[str, Module]:
        loaded = {}
        if "base" in modules:
            raise Exception("Don't load base module!")

        for name in modules:
            try:
                module = importlib.import_module(f"otoposuto.modules.{name.lower()}")
                cls = getattr(module, f"{name.capitalize()}Module")
                loaded[name] = cls()
            except Exception as e:
                print(
                    f"{red_color}Failed to load module {yellow_color}{name}{red_color} with error: {yellow_color}{e}{reset_color}"
                )
        return loaded
