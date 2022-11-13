from abc import abstractmethod


class TranslationInterface:
    @abstractmethod
    def translate(self, message: str) -> str:
        """Translate a message"""

    @abstractmethod
    def load_translation(self, country: str) -> None:
        """Load a translation"""
