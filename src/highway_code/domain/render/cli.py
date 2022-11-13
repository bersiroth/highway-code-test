from abc import abstractmethod


class CliRenderInterface:
    @abstractmethod
    def echo(self, message: str) -> None:
        """Print a message to the console"""

    @abstractmethod
    def echo_color(self, message: str, color: str) -> None:
        """Print a message to the console with a color"""

    @abstractmethod
    def message_color(self, message: str, color: str) -> str:
        """Return a message with a color"""

    @abstractmethod
    def get_input(self, message: str) -> str:
        """Return the input of the user"""

    @abstractmethod
    def confirm(self, message: str) -> bool:
        """Return the confirmation of the user"""
