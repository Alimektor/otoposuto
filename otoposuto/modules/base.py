from abc import ABC, abstractmethod


class Module(ABC):
    @abstractmethod
    def post(self, content: str, filename: str) -> bool:
        pass

    @abstractmethod
    def change(self, content: str, filename: str) -> bool:
        pass

    @abstractmethod
    def prompt_metadata(self, config: dict) -> dict:
        return {}
