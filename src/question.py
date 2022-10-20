"""
Question logic
"""
from __future__ import annotations

import os
import json
import random
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional, ClassVar
import click
from typing_extensions import TypeGuard

from stats import Stats


@dataclass
class Title:
    """
    Title class
    """

    principal: str
    sub: List[str | None]


@dataclass
class Question:
    """
    Question class
    """

    __question_id: int
    __title: Title
    __propositions: List[str]
    __responses: List[str]
    __explication: str
    __labels: ClassVar[Tuple[str, str, str, str]] = ("A", "B", "C", "D")

    @property
    def question_id(self) -> int:
        """
        Question id getter
        """
        return self.__question_id

    def render(self) -> None:
        """
        Render cli question
        """
        self.__render_question()
        self.__render_propositions()

    def __render_propositions(self):
        if len(self.__title.sub) > 0:
            click.echo(self.__title.sub[0])
        propositions = self.__propositions
        max_proposition_len = len(propositions[0]) + 10
        self.__render_proposition(self.__labels[:2], max_proposition_len, propositions[:2])
        if len(propositions) > 2:
            if len(self.__title.sub) > 1:
                click.echo()
                click.echo(self.__title.sub[1])
            self.__render_proposition(self.__labels[2:], max_proposition_len, propositions[2:])
        click.echo()

    def __render_question(self):
        click.echo("\n\n")
        question = click.style(self.__title.principal, fg="white")
        size = len(question)
        try:
            size_terminal = os.get_terminal_size()
            size = size_terminal.columns
        except OSError:
            print("get_terminal_size is not supported")
        line = "".ljust(size, "-")
        click.secho(line, fg="blue")
        click.secho(f"(Question {self.__question_id}) : {question}", fg="blue")
        click.secho(line, fg="blue")

    def __render_proposition(self, labels: Tuple[str], max_proposition_len: int, propositions: List[str]) -> None:
        if len(propositions) == 1:
            click.echo(self.__format_proposition(propositions[0], max_proposition_len, labels[0]))
            return

        rendered_proposition = []
        for key, proposition in enumerate(propositions):
            rendered_proposition.append(self.__format_proposition(proposition, max_proposition_len, labels[key]))
        click.echo(f"{rendered_proposition[0]} {rendered_proposition[1]}")

    def __format_proposition(self, proposition: str, proposition_len: int, label: str) -> str:
        label = click.style(label, fg="yellow")
        label_rendered = f"[{label}]"
        return f"{label_rendered} {proposition.ljust(proposition_len, ' ')}"

    def __validate_answer(self, answer: str) -> bool:
        responses = ",".join(self.__responses).lower()
        is_correct = answer.lower() == responses
        if is_correct:
            click.secho("Correct !", fg="green")
        else:
            click.secho(f"Wrong ! The good answer is {responses.upper()}.", err=True, fg="red")

        click.echo()
        size = len(self.__explication)
        try:
            size_terminal = os.get_terminal_size()
            size = size_terminal.columns
        except OSError:
            print("get_terminal_size is not supported")
        line = "".ljust(size, "-")
        click.secho(line, fg="cyan")
        click.secho(self.__explication.replace(". ", ".\n"), fg="cyan")
        click.secho(line, fg="cyan")
        click.echo()
        return is_correct

    def answer(self) -> bool:
        """
        Get and validate answer from prompt
        """
        message = "Enter your answer with label letter separated by comma. (Ex: A,C)"
        prompt = click.style(message, fg="yellow")
        while True:
            input_answer = click.prompt(prompt, type=str)
            answers = input_answer.replace(" ", "")
            if not self.__check_if_answer_is_a_label(answers):
                continue
            break

        return self.__validate_answer(input_answer)

    def __check_if_answer_is_a_label(self, answers: str) -> bool:
        labels = self.__labels[: len(self.__propositions)]
        for answer in answers.split(","):
            if answer.upper() not in labels:
                click.secho(f"ERROR: {answer} is not in labels ({','.join(labels)}), try again.", fg="red")
                return False
        return True


class QuestionList:
    """
    Load question list from json file
    """

    __questions_list: List[Question]

    def __init__(self) -> None:
        self.__questions_list = self.__load_questions_list()

    def __load_questions_list(self) -> List[Question]:
        with open("data/questions.json", "r", encoding="utf-8") as openfile:
            questions = json.load(openfile)
            question_list = []
            for question in questions:
                try:
                    question_list.append(
                        Question(
                            question["id"],
                            Title(
                                question["title"]["principal"],
                                question["title"]["sub"] if "sub" in question["title"] else [],
                            ),
                            question["propositions"],
                            question["responses"],
                            question["explication"],
                        )
                    )
                except KeyError as error:
                    print(repr(error))
                    print(question)

            return question_list

    def __get_question(self, question_id: int) -> Question | None:
        """
        Get question by id
        """

        def question_filter(question: Question) -> TypeGuard[Optional[Question]]:
            return question.question_id == question_id

        return next(filter(question_filter, self.__questions_list), None)

    def __get_random_question(self) -> Question:
        """
        Get random question from list
        """
        system_random = random.SystemRandom()
        questions_list = self.__questions_list
        rand_int = system_random.randint(0, len(questions_list) - 1)
        question = questions_list[rand_int]
        questions_list.remove(question)
        return question

    def is_empty(self) -> bool:
        """
        Check if list is empty
        """
        return len(self.__questions_list) == 0

    def select_question(self, question_id: int | None) -> Question:
        """
        Select good question
        """
        if question_id is not None:
            question = self.__get_question(question_id)
            if question is None:
                click.secho(f"Question id {question_id} not found.", fg="red")
                sys.exit(1)
            return question
        return self.__get_random_question()


def question_process(stop_on_failure: bool = False, question_id: int | None = 1) -> None:
    """
    Question process, load list, get random question, answer, show stats, etc ...
    """
    question_list = QuestionList()
    stats = Stats()
    new_question = True
    is_correct = False

    while new_question:
        question = question_list.select_question(question_id)
        question.render()
        is_correct = question.answer()
        stats.add_answer(is_correct)
        if question_list.is_empty() or (not is_correct and stop_on_failure) or question_id is not None:
            break
        label = click.style("New question ?", fg="yellow")
        new_question = click.confirm(label, default=None)
        click.echo()

    click.echo()
    if question_list.is_empty():
        click.echo("Congratulation ! You have answer to all questions\n")
    stats.render()
    stats.save()

    if not is_correct and stop_on_failure:
        sys.exit(1)
