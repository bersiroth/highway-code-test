"""
Statistique logic
"""
from __future__ import annotations

from os.path import exists
from typing import TypedDict
from datetime import date
import json
import click


class StatsDict(TypedDict):
    """
    Stat dict
    """

    answer: int
    correct: int
    wrong: int
    last: str


class Stats:
    """
    Stats class
    """

    __session: StatsDict
    __global: StatsDict
    __default_stats: StatsDict = {
        "answer": 0,
        "correct": 0,
        "wrong": 0,
        "last": "1999-01-01",
    }
    __line: str = "".ljust(46, "-")

    def __init__(self, restart: bool = False) -> None:
        self.__global = self.__load_stats(restart)
        self.__session = self.__default_stats.copy()
        if restart:
            self.save()

    def __load_stats(self, restart: bool = False) -> StatsDict:
        file = "data/stats.json"
        if not exists(file) or restart:
            return self.__default_stats.copy()
        with open(file, "r", encoding="utf-8") as openfile:
            return json.load(openfile)

    def render(self) -> None:
        """
        Render cli stats
        """
        click.echo()
        self.__render_title("Statistics", False)
        if self.__session["answer"] > 0:
            self.__render_session()
        self.__render_global()
        click.echo()

    def __render_global(self):
        self.__render_title("Global")
        self.__render_data("Total answer", self.__global["answer"])
        self.__render_data("Total correct answer", self.__global["correct"])
        self.__render_data("Total wrong answer", self.__global["wrong"])
        if self.__global["answer"] > 0:
            self.__render_data(
                "Percentage correct", str(round((self.__global["correct"] / self.__global["answer"]) * 100, 2)) + "%"
            )
        self.__render_data("Last answer date", self.__global["last"])
        click.echo("   " + self.__line)

    def __render_title(self, title: str, bottom_line: bool = True):
        click.echo("   " + self.__line)
        title = click.style(title.center(44, " "), fg="blue")
        click.echo(f"   |{title}|")
        if bottom_line:
            click.echo("   " + self.__line)

    def __render_session(self):
        self.__render_title("Session")
        self.__render_data("Total answer", self.__session["answer"])
        self.__render_data("Total correct answer", self.__session["correct"])
        self.__render_data("Total wrong answer", self.__session["wrong"])
        self.__render_data(
            "Percentage correct", str(round((self.__session["correct"] / self.__session["answer"]) * 100, 2)) + "%"
        )

    def __render_data(self, label: str, data: int | str) -> None:
        label = click.style(label, fg="yellow").ljust(30, " ")
        label_rendered = f"   | {label}"
        click.echo(label_rendered + "   | " + str(data).ljust(17, " ") + "|")

    def add_answer(self, is_correct: bool) -> None:
        """
        Add answer to stats
        """
        self.__global["answer"] += 1
        self.__session["answer"] += 1
        if is_correct:
            self.__global["correct"] += 1
            self.__session["correct"] += 1
        else:
            self.__global["wrong"] += 1
            self.__session["wrong"] += 1
        self.__global["last"] = date.today().isoformat()

    def save(self) -> None:
        """
        Save stats in file
        """
        with open("data/stats.json", "w+", encoding="utf-8") as openfile:
            json.dump(self.__global, openfile)
