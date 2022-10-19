import os
from typing import List
from stats import Stats
from sys import exit
import json
import random
import click


class Question:

    __id: int
    __question: str
    __propositions: List[str]
    __responses: List[str]
    __explication: str
    labels: List[str] = ["A", "B", "C", "D"]

    def __init__(self, id: int, question: str, propositions: List[str], responses: List[str], explication: str) -> None:
        self.__id = id
        self.__question = question
        self.__propositions = propositions
        self.__responses = responses
        self.__explication = explication

    def render(self) -> None:
        self.__render_question()
        self.__render_propositions()

    def __render_propositions(self):
        propositions = self.__propositions
        max_proposition_len = len(propositions[0]) + 10
        self.__render_proposition(self.labels[:2], max_proposition_len, propositions[:2])
        if len(propositions) > 2:
            self.__render_proposition(self.labels[2:], max_proposition_len, propositions[2:])
        click.echo()

    def __render_question(self):
        click.echo("\n\n")
        question = click.style(self.__question, fg="white")
        size = len(question)
        try:
            size_terminal = os.get_terminal_size()
            size = size_terminal.columns
        except OSError:
            print("get_terminal_size is not supported")
        line = "".ljust(size, "-")
        click.secho(line, fg="blue")
        click.secho(f"(Question {self.__id}) : {question} ?", fg="blue")
        click.secho(line, fg="blue")

    def __render_proposition(self, labels: List[str], max_proposition_len: int, propositions: List[str]) -> None:
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

    def validate_answer(self, answer: str) -> bool:
        responses = ",".join(self.__responses).lower()
        is_correct = answer.lower() == responses
        if is_correct:
            click.secho("Correct !", fg="green")
        else:
            click.secho(f"Wrong ! The good answer is {responses.upper()}.", err=True, fg="red")

        click.echo()
        click.secho(self.__explication.replace(". ", ".\n"), fg="cyan")
        click.echo()
        return is_correct

    def get_answer(self) -> str:
        message = "Enter your answer with label letter separated by comma. (Ex: A,C)"
        prompt = click.style(message, fg="yellow")
        while True:
            input_answer = click.prompt(prompt, type=str)
            answers = input_answer.replace(" ", "")
            if not self.__check_if_answer_is_a_label(answers):
                continue
            break

        return input_answer

    def __check_if_answer_is_a_label(self, answers: str) -> bool:
        labels = self.labels[: len(self.__propositions)]
        for answer in answers.split(","):
            if answer.upper() not in labels:
                click.secho(f"ERROR: {answer} is not in labels ({','.join(labels)}), try again.", fg="red")
                return False
        return True


class QuestionList:
    __questions_list: List[Question]

    def __init__(self) -> None:
        self.__questions_list = self.__load_questions_list()

    def __load_questions_list(self) -> List[Question]:
        with open("data/questions.json", "r") as openfile:
            questions = json.load(openfile)
            question_list = []
            for question in questions:
                try:
                    question_list.append(
                        Question(
                            question["id"],
                            question["question"],
                            question["propositions"],
                            question["responses"],
                            question["explication"],
                        )
                    )
                except Exception as e:
                    print(repr(e))
                    print(question)

            return question_list

    def get_random_question(self) -> Question:
        question = random.choice(self.__questions_list)
        self.__questions_list.remove(question)
        return question

    def is_empty(self) -> bool:
        return len(self.__questions_list) == 0


def question_process(stop_on_failure: bool = False) -> None:
    question_list = QuestionList()
    stats = Stats()
    new_question = True
    while new_question:
        question = question_list.get_random_question()
        question.render()
        answer = question.get_answer()
        is_correct = question.validate_answer(answer)
        stats.add_answer(is_correct)
        if not is_correct and stop_on_failure:
            stats.render()
            stats.save()
            exit(1)
        if question_list.is_empty():
            break
        label = click.style("New question ?", fg="yellow")
        new_question = click.confirm(label, default=None)
        click.echo()

    click.echo("\n\n")
    if question_list.is_empty():
        click.echo("Congratulation ! You have answer to all questions\n")
    stats.render()
    stats.save()
