"""
Model question
"""
from __future__ import annotations

import os

from highway_code.domain.model.question import Question
from highway_code.domain.render.cli import CliRenderInterface


class CliRenderQuestion:
    __cli_render: CliRenderInterface

    def __init__(self, cli_render: CliRenderInterface):
        self.__cli_render = cli_render

    def show_question(self, question: Question) -> None:
        self.render_title(question)
        self.render_propositions(question)

    def render_title(self, question: Question) -> None:
        self.__cli_render.echo("\n\n")
        question_title = self.__cli_render.message_color(question.title.principal, "white")
        size = len(question_title)
        try:
            size_terminal = os.get_terminal_size()
            size = size_terminal.columns
        except OSError:
            print("get_terminal_size is not supported")
        line = "".ljust(size, "-")
        self.__cli_render.echo_color(line, "blue")
        self.__cli_render.echo_color(f"(Question {question.question_id}) : {question_title}", "blue")
        self.__cli_render.echo_color(line, "blue")

    def render_propositions(self, question: Question) -> None:
        propositions = question.propositions
        max_proposition_len = len(propositions[0]) + 10
        rendered_proposition = []
        for key, proposition in enumerate(propositions):
            label = self.__cli_render.message_color(question.labels[key], "yellow")
            label_rendered = f"[{label}]"
            rendered_proposition.append(f"{label_rendered} {proposition.ljust(max_proposition_len, ' ')}")

        sub_title_list = question.title.sub
        if len(sub_title_list) > 0:
            self.__cli_render.echo(sub_title_list[0])
        self.__cli_render.echo(f"{rendered_proposition[0]} {rendered_proposition[1]}")

        if len(propositions) == 2:
            return

        if len(sub_title_list) == 2:
            self.__cli_render.echo(sub_title_list[1])
        if len(propositions) == 4:
            self.__cli_render.echo(f"{rendered_proposition[2]} {rendered_proposition[3]}")
        else:
            self.__cli_render.echo(f"{rendered_proposition[2]}")

    def render_correction(self, question: Question, message: str, is_correct_answer: bool):
        color = "green" if is_correct_answer else "red"
        size = len(message) + 4
        line = "".ljust(size, "-")
        self.__cli_render.echo_color(line, color)
        self.__cli_render.echo_color("| " + message + " |", color)
        self.__cli_render.echo_color(line + '\n', color)
        self.render_explication(question)

    def render_explication(self, question: Question):
        size = len(question.explication)
        try:
            size_terminal = os.get_terminal_size()
            size = size_terminal.columns
        except OSError:
            print("get_terminal_size is not supported")
        line = "".ljust(size, "-")
        self.__cli_render.echo_color(line, "cyan")
        self.__cli_render.echo_color(question.explication.replace(". ", ".\n"), "cyan")
        self.__cli_render.echo_color(line, "cyan")


class CliRenderQuestionManager:
    __cli_render: CliRenderInterface

    def __init__(self, cli_render: CliRenderInterface):
        self.__cli_render = cli_render

    def ask_answer(self, message: str) -> str:
        message = self.__cli_render.message_color(message, "yellow")
        input_answer = self.__cli_render.get_input(message)
        return input_answer.replace(" ", "")

    def render_error(self, error: str) -> None:
        self.__cli_render.echo_color(error, 'red')

    def ask_question_again(self, message: str) -> bool:
        message = self.__cli_render.message_color(message, "yellow")
        return self.__cli_render.confirm(message)

    def show_congratulation(self, message: str) -> None:
        self.__cli_render.echo(message)
