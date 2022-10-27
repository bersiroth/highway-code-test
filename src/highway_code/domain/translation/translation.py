"""
Translation logic
"""
from abc import abstractmethod


class TranslationInterface:
    @abstractmethod
    def translate(self, message: str) -> str:
        pass

    @abstractmethod
    def load_translation(self, country: str) -> None:
        pass