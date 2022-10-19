from __future__ import annotations

from os.path import exists
from typing import TypedDict
from datetime import date
import json
import click


class Stat(TypedDict):
    answer: int
    correct: int
    wrong: int
    last: str


class Stats:

    __answer: int
    __correct: int
    __wrong: int
    __last: str
    session: Stat
    default_stats: Stat = {
        "answer": 0,
        "correct": 0,
        "wrong": 0,
        "last": "1999-01-01",
    }
    line: str = "".ljust(46, "-")

    def __init__(self, restart: bool = False) -> None:
        stats = self.__load_stats(restart)
        self.__answer = stats["answer"]
        self.__correct = stats["correct"]
        self.__wrong = stats["wrong"]
        self.__last = stats["last"]
        self.session = self.default_stats.copy()
        if restart:
            self.save()

    def __load_stats(self, restart: bool = False) -> Stat:
        file = "data/stats.json"
        if not exists(file) or restart:
            return self.default_stats
        with open(file, "r") as openfile:
            return json.load(openfile)

    def render(self) -> None:
        click.echo()
        self.__render_title("Statistics", False)
        if self.session["answer"] > 0:
            self.__render_session()
        self.__render_global()
        click.echo()

    def __render_global(self):
        self.__render_title("Global")
        self.render_data("Total answer", self.__answer)
        self.render_data("Total correct answer", self.__correct)
        self.render_data("Total wrong answer", self.__wrong)
        if self.__answer > 0:
            self.render_data("Percentage correct", str(round((self.__correct / self.__answer) * 100, 2)) + "%")
        self.render_data("Last answer date", self.__last)
        click.echo("   " + self.line)

    def __render_title(self, title: str, bottom_line: bool = True):
        click.echo("   " + self.line)
        title = click.style(title.center(44, " "), fg="blue")
        click.echo(f"   |{title}|")
        if bottom_line:
            click.echo("   " + self.line)

    def __render_session(self):
        self.__render_title("Session")
        self.render_data("Total answer", self.session["answer"])
        self.render_data("Total correct answer", self.session["correct"])
        self.render_data("Total wrong answer", self.session["wrong"])
        self.render_data(
            "Percentage correct", str(round((self.session["correct"] / self.session["answer"]) * 100, 2)) + "%"
        )

    def render_data(self, label: str, data: int | str) -> None:
        label = click.style(label, fg="yellow").ljust(30, " ")
        label_rendered = f"   | {label}"
        click.echo(label_rendered + "   | " + str(data).ljust(17, " ") + "|")

    def add_answer(self, is_correct: bool) -> None:
        self.__answer += 1
        self.session["answer"] += 1
        if is_correct:
            self.__correct += 1
            self.session["correct"] += 1
        else:
            self.__wrong += 1
            self.session["wrong"] += 1
        self.__last = date.today().isoformat()

    def save(self) -> None:
        with open("data/stats.json", "w+") as openfile:
            json.dump(
                {
                    "answer": self.__answer,
                    "correct": self.__correct,
                    "wrong": self.__wrong,
                    "last": self.__last,
                },
                openfile,
            )
