from __future__ import annotations

from highway_code.domain.model.statistic import Statistic
from highway_code.domain.render.cli import CliRenderInterface


class CliRenderStatistic:
    __line: str = "".ljust(46, "-")

    def __init__(self, cli_render: CliRenderInterface):
        self.cli_render = cli_render

    def render_all_statistics(self, _global: Statistic, session: Statistic) -> None:
        self.cli_render.echo("   " + self.__line)
        title = self.cli_render.message_color("Statistics".center(44, " "), "blue")
        self.cli_render.echo(f"   |{title}|")

        if not session.is_empty():
            self.cli_render.echo("   " + self.__line)
            title = self.cli_render.message_color("Session".center(44, " "), "blue")
            self.cli_render.echo(f"   |{title}|")
            self.cli_render.echo("   " + self.__line)
            self.render_statistic(session, show_date=False)

        self.cli_render.echo("   " + self.__line)
        title = self.cli_render.message_color("Global".center(44, " "), "blue")
        self.cli_render.echo(f"   |{title}|")
        self.cli_render.echo("   " + self.__line)
        self.render_statistic(_global)
        self.cli_render.echo("   " + self.__line)

    def render_statistic(self, statistic: Statistic, show_date: bool = True) -> None:
        self.render_single_statistic("Total answer", statistic.answer)
        self.render_single_statistic("Total correct answer", statistic.correct)
        self.render_single_statistic("Total wrong answer", statistic.wrong)
        if statistic.answer > 0:
            self.render_single_statistic(
                "Percentage correct", str(round((statistic.correct / statistic.answer) * 100, 2)) + "%"
            )
        if show_date:
            self.render_single_statistic("Last answer date", statistic.last)

    def render_single_statistic(self, label: str, data: int | str) -> None:
        label = self.cli_render.message_color(label, "yellow").ljust(30, " ")
        label_rendered = f"   | {label}"
        self.cli_render.echo(label_rendered + "   | " + str(data).ljust(17, " ") + "|")
