from datetime import datetime
import os
from otoposuto.modules.base import Module
from otoposuto.utils import m_print, m_input
from otoposuto.colors import blue_color


class HugoModule(Module):
    def post(self, content: str, filename: str, metadata: dict) -> bool:
        try:
            content_dir = os.path.expanduser(metadata["content_dir"])
            m_print(f"Content directory: {blue_color}{content_dir}")
            os.makedirs(content_dir, exist_ok=True)
            post_metadata = metadata["metadata"]
            slug = filename.replace(".md", "")
            date = datetime.now().strftime("%Y-%m-%d")
            post_filename = f"{date}-{slug}.md"
            post_path = os.path.join(content_dir, post_filename)
            m_print(f"Writing post to: {blue_color}{post_path}")
            with open(post_path, "w") as f:
                f.write(f"---\n")
                for key, value in post_metadata.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"---\n\n")
                f.write(content)
            m_print(f"Created: {blue_color}{post_path}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def change(self, content: str, metadata: dict, filename: str) -> bool:
        m_print(f"Changing: {blue_color}{filename}")
        return self.post(content, filename, metadata)

    def prompt_metadata(self, config: dict) -> dict:
        m_print("Prompting metadata...")
        hugo_metadata = {**config}
        for key, value in hugo_metadata["metadata"].items():
            if isinstance(value, str):
                value = m_input(f"Prompt for {key} [{value}]: ")
            if isinstance(value, list):
                current_value = m_input(
                    f"Prompt for {key} [{', '.join(value)}] (separated by comma): "
                )
                if len(current_value) > 0:
                    value = [tag.strip() for tag in current_value.split(",")]
            if isinstance(value, bool):
                value = m_input(f"Prompt for {key} [{value}] (yes/no): ")
                if value == "yes":
                    value = True
                else:
                    value = False
            if value:
                hugo_metadata["metadata"][key] = value
        hugo_metadata["date"] = datetime.now().strftime("%Y-%m-%d")
        m_print(f"Metadata: {blue_color}{hugo_metadata}")
        return hugo_metadata
