"""
List all commands.
"""
import click

from question import question_process
from stats import Stats


@click.group()
def cli():
    """CLI application for highway code practice."""


@cli.command("question")
@click.option(
    "-s",
    "--stop-on-failure",
    "stop_on_failure",
    is_flag=True,
    default=False,
    show_default=True,
    help="Set if application must stop on first failure.",
)
@click.option(
    "--id",
    "question_id",
    type=int,
    help="Select question by id.",
)
def question(stop_on_failure, question_id):
    """Answer to a question."""
    question_process(stop_on_failure, question_id)


@cli.command("stats")
@click.option(
    "--reset",
    is_flag=True,
    help="If you want reset your statistics",
)
def stats(reset):
    """View statistics."""
    my_stats = Stats(reset)
    my_stats.render()


if __name__ == "__main__":
    cli()
