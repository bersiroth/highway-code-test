"""
Click cli render
"""
import click

from highway_code.domain.render.cli import CliRenderInterface


class ClickCliRender(CliRenderInterface):
    def echo(self, message: str) -> None:
        click.echo(message)

    def echo_color(self, message: str, color: str) -> None:
        click.secho(message, fg=color)

    def message_color(self, message: str, color: str) -> str:
        return click.style(message, fg=color)

    def get_input(self, message: str) -> str:
        return click.prompt(message, type=str)

    def confirm(self, message: str) -> bool:
        return click.confirm(message, default=None)
