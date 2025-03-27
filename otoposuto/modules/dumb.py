from otoposuto.modules.base import Module
from otoposuto.utils import m_print, m_input
from otoposuto.colors import blue_color


class DumbModule(Module):
    def post(self, content: str, metadata: dict, filename: str) -> bool:
        m_print(f"Posted: {blue_color}{filename}")
        m_print(f"Metadata: {blue_color}{metadata}")
        m_print(f"Content:\n{blue_color}{content}")
        return True

    def change(self, content: str, metadata: dict, filename: str) -> bool:
        m_print(f"Changed: {blue_color}{filename}")
        m_print(f"Metadata: {blue_color}{metadata}")
        m_print(f"Content:\n{blue_color}{content}")
        return True

    def prompt_metadata(self, config: dict) -> dict:
        m_print("Prompting metadata...")
        return {
            "title": config["title"] if config["title"] else m_input("Title:"),
            "description": (
                config["description"]
                if config["description"]
                else m_input("Description:")
            ),
        }
