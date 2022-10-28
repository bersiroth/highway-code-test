from __future__ import annotations

import sys

import click
from dependency_injector.wiring import Provide, inject

from highway_code.application.question.handler import QuestionCommand, QuestionHandler
from highway_code.application.statistic.handler import (
    StatisticCommand,
    StatisticHandler,
)
from highway_code.infrastructure.containers import Container


@click.group()
def cli():
    container = Container()
    container.init_resources()
    container.wire(modules=[sys.modules[__name__]])


@cli.command("question")
@click.option(
    "-e",
    "--error_on_failure",
    "error_on_failure",
    is_flag=True,
    default=False,
    show_default=True,
    help="Set if application must error on failure.",
)
@click.option(
    "--id",
    "question_id",
    type=int,
    help="Select question by id.",
)
@click.option(
    "--country",
    default="fr",
    help="Select country.",
)
@inject
def question(
    error_on_failure: bool,
    question_id: int | None,
    country: str,
    question_handler: QuestionHandler = Provide[Container.question_handler],
):
    command = QuestionCommand(question_id, country, error_on_failure)
    question_handler.handle(command)


@cli.command("stats")
@click.option(
    "--reset",
    is_flag=True,
    help="If you want reset your statistics",
)
@inject
def stats(reset, statistic_handler: StatisticHandler = Provide[Container.statistic_handler]):
    command = StatisticCommand(reset)
    statistic_handler.handle(command)


if __name__ == "__main__":
    cli()
