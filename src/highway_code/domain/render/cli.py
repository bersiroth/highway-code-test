"""
Cli render interface
"""
from abc import abstractmethod


class CliRenderInterface:

    @abstractmethod
    def echo(self, message: str) -> None:
        pass
    
    @abstractmethod
    def echo_color(self, message: str, color: str) -> None:
        pass

    @abstractmethod
    def message_color(self, message: str, color: str) -> str:
        pass

    @abstractmethod
    def get_input(self, message: str) -> str:
        pass

    @abstractmethod
    def confirm(self, message: str) -> bool:
        pass
