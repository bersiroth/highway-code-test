from unittest.mock import Mock

import pytest
from _pytest.capture import CaptureFixture

from highway_code.domain.question.render import (
    CliRenderQuestion,
    CliRenderQuestionManager,
)
from highway_code.domain.render.cli import CliRenderInterface
from tests.unit.factory import question_factory_test


def get_cli_render_mock() -> CliRenderInterface:
    cli_render_mock = Mock(spec_set=CliRenderInterface)
    cli_render_mock.message_color.side_effect = lambda message, color: message
    cli_render_mock.echo_color.side_effect = lambda message, color: print(message)
    cli_render_mock.echo.side_effect = lambda message: print(message)

    def get_input_mock(message: str) -> str:
        print(message)
        return "A"

    cli_render_mock.get_input.side_effect = get_input_mock

    def confirm_mock(message: str) -> bool:
        print(message)
        return True

    cli_render_mock.confirm.side_effect = confirm_mock
    return cli_render_mock


@pytest.fixture
def cli_render_question() -> CliRenderQuestion:
    return CliRenderQuestion(get_cli_render_mock())


@pytest.fixture
def cli_render_question_manager() -> CliRenderQuestionManager:
    return CliRenderQuestionManager(get_cli_render_mock())


def test_render_title(cli_render_question: CliRenderQuestion, capsys: CaptureFixture[str]) -> None:
    # Given: I have a question
    question = question_factory_test()
    # When: I want to render the title
    cli_render_question.render_title(question)
    # Then: I have a good title render
    captured = capsys.readouterr()
    expected_render = """\

----------------------------------------------------------------
(Question 1) : Les feux de recul d'un véhicule sont de couleur ?
----------------------------------------------------------------
"""
    assert expected_render in captured.out


def test_render_propositions(cli_render_question: CliRenderQuestion, capsys: CaptureFixture[str]) -> None:
    # Given: I have a question
    question = question_factory_test(
        propositions=["oui", "non", "peut-être"], sub_title=["Sub question 1 ?", "Sub question 2 ?"]
    )
    # When: I want to render the propositions
    cli_render_question.render_propositions(question)
    # Then: I have a good propositions render
    captured = capsys.readouterr()
    expected_render = """\
Sub question 1 ?
[A] oui           [B] non
Sub question 2 ?
[C] peut-être
"""
    assert expected_render in captured.out


def test_render_propositions_without_sub_title(
    cli_render_question: CliRenderQuestion, capsys: CaptureFixture[str]
) -> None:
    # Given: I have a question
    question = question_factory_test(propositions=["oui", "non", "peut-être", "je ne sais pas"])
    # When: I want to render the propositions
    cli_render_question.render_propositions(question)
    # Then: I have a good propositions render
    captured = capsys.readouterr()
    expected_render = """\
[A] oui           [B] non
[C] peut-être     [D] je ne sais pas
"""
    assert expected_render in captured.out


def test_render_correction(cli_render_question: CliRenderQuestion, capsys: CaptureFixture[str]) -> None:
    # Given: I have a question
    question = question_factory_test()
    # When: I want to render the correction
    cli_render_question.render_correction(question, "correct", True)
    # Then: I have a good correction render
    captured = capsys.readouterr()
    expected_render = """\
-----------
| correct |
-----------
"""
    assert expected_render in captured.out


def test_render_explication(cli_render_question: CliRenderQuestion, capsys: CaptureFixture[str]) -> None:
    # Given: I have a question
    question = question_factory_test()
    # When: I want to render the explication
    cli_render_question.render_explication(question)
    # Then: I have a good explication render
    captured = capsys.readouterr()
    expected_render = """\
--------------------------------------------------------
Les feux de recul d'un véhicule sont de couleur blanche.
--------------------------------------------------------
"""
    assert expected_render in captured.out


def test_ask_answer(cli_render_question_manager: CliRenderQuestionManager, capsys: CaptureFixture[str]) -> None:
    # Given: I have a question
    question = "Enter your answer with label letter separated by comma. (Ex: A,C)"
    # When: I want to render
    cli_render_question_manager.ask_answer(question)
    # Then: I have a good render
    captured = capsys.readouterr()
    expected_render = """\
Enter your answer with label letter separated by comma. (Ex: A,C)
"""
    assert expected_render in captured.out


def test_render_error(cli_render_question_manager: CliRenderQuestionManager, capsys: CaptureFixture[str]) -> None:
    # Given: I have a message
    message = "Question id 1 not found."
    # When: I want to render
    cli_render_question_manager.render_error(message)
    # Then: I have a good render
    captured = capsys.readouterr()
    expected_render = """\
Question id 1 not found.
"""
    assert expected_render in captured.out


def test_ask_question_again(cli_render_question_manager: CliRenderQuestionManager, capsys: CaptureFixture[str]) -> None:
    # Given: I have a message
    message = "New question ?"
    # When: I want to render
    cli_render_question_manager.ask_question_again(message)
    # Then: I have a good render
    captured = capsys.readouterr()
    expected_render = """\
New question ?
"""
    assert expected_render in captured.out


def test_show_congratulation(
    cli_render_question_manager: CliRenderQuestionManager, capsys: CaptureFixture[str]
) -> None:
    # Given: I have a message
    message = "Congratulation ! You have answer to all questions"
    # When: I want to render
    cli_render_question_manager.show_congratulation(message)
    # Then: I have a good render
    captured = capsys.readouterr()
    expected_render = """\
Congratulation ! You have answer to all questions
"""
    assert expected_render in captured.out
