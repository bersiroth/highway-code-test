from __future__ import annotations

import pytest
from click.testing import Result
from pytest import fixture

from highway_code.domain.question.exception import BadCountryException
from highway_code.infrastructure.cli import command
from highway_code.infrastructure.containers import Container
from tests.functional.cli.command_helper import run_command_with_fixture


@fixture(scope="session", autouse=True)
def init_container():
    container = Container()
    container.init_resources()
    container.wire(modules=[command])


def run_question_command(
    input_sequence: str = "a\nn\n",
    error_on_failure: bool = False,
    question_id: int | None = None,
    country: str | None = None,
) -> Result:
    args = []
    if error_on_failure:
        args.append("--error_on_failure")
    if question_id:
        args.append("--id")
        args.append(str(question_id))
    if country:
        args.append("--country")
        args.append(str(country))
    return run_command_with_fixture("question", args, input_sequence)


def test_question_command_with_correct_answer() -> None:
    # Given : I have valid input
    input_sequence = "b\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "Les feux de recul d'un véhicule sont de couleur ?" in result.output
    assert "[A] Rouge           [B] Blanche" in result.output
    assert (
        "Enter votre réponse en utilisant les lettres des labels en les séparant avec une virgule. (Ex: A,C): b"
        in result.output
    )
    assert "Correct !" in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "Nouvelle question ? [y/n]: n" in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 1" in result.output
    assert "Total wrong answer      | 0" in result.output


def test_question_command_with_wrong_answer_with_error_on_failure() -> None:
    # Given : I have valid input
    input_sequence = "a\nn\n"
    error_on_failure = True
    # When : I run question command with input
    result = run_question_command(input_sequence, error_on_failure)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 1
    assert (
        "Enter votre réponse en utilisant les lettres des labels en les séparant avec une virgule. (Ex: A,C): a"
        in result.output
    )
    assert "Faux ! La bonne réponse est B." in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 1" in result.output


def test_question_command_with_wrong_answer() -> None:
    # Given : I have valid input
    input_sequence = "a\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert (
        "Enter votre réponse en utilisant les lettres des labels en les séparant avec une virgule. (Ex: A,C): a"
        in result.output
    )
    assert "Faux ! La bonne réponse est B." in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 1" in result.output


def test_question_command_with_wrong_label() -> None:
    # Given : I have input with invalid label
    input_sequence = "e\na\nn\n"
    question_id = 2
    # When : I run question command with input
    result = run_question_command(input_sequence, question_id=question_id)
    # Then : Command has no error and I have error message for invalid label
    assert result.exit_code == 0
    assert "ERREUR: e n'est pas un label valide (A,B), essayez encore." in result.output


def test_question_command_with_multiple_question() -> None:
    # Given : I have valid input for two questions
    input_sequence = "b\ny\nb\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "Nouvelle question ? [y/n]: n" in result.output
    assert "Total answer            | 2" in result.output
    assert "Total correct answer    | 2" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Félicitation ! Vous avez répondu a toutes les questions" not in result.output


def test_question_command_with_all_questions() -> None:
    # Given : I have valid input for two questions
    input_sequence = "b\ny\nb\ny\na\ny\na\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "Nouvelle question ? [y/n]: y" in result.output
    assert "Total answer            | 4" in result.output
    assert "Total correct answer    | 2" in result.output
    assert "Total wrong answer      | 2" in result.output
    assert "Félicitation ! Vous avez répondu a toutes les questions" in result.output


def test_question_command_with_question_id() -> None:
    # Given : I have question id
    question_id = 2
    # When : I run question command with question id
    result = run_question_command(question_id=question_id)
    # Then : Command has no error and I have the good question in output
    assert result.exit_code == 0
    assert "(Question 2) : Les feux de recul d'un véhicule sont de couleur ?" in result.output
    assert "Nouvelle question ? [y/n]:" not in result.output


def test_question_command_with_sub_title() -> None:
    # Given : I have id for question with sub label
    question_id = 4
    # When : I run question command with question id
    result = run_question_command(question_id=question_id)
    # Then : Command has no error and I have the good question in output
    assert result.exit_code == 0
    assert "(Question 4) : Les feux de recul d'un véhicule sont de couleur ?" in result.output
    assert "En hauteur ?" in result.output
    assert "En profondeur ?" in result.output
    assert "Nouvelle question ? [y/n]:" not in result.output


def test_question_command_with_en_country() -> None:
    # Given : I have a country
    country = "en"
    # When : I run question command with country
    result = run_question_command(country=country)
    # Then : Command has no error and I have the good question in output
    assert result.exit_code == 0
    assert "(Question 1) : The reversing lights of a vehicle are colored ?" in result.output
    assert "Enter your answer with label letter separated by comma. (Ex: A,C): a" in result.output
    assert "Wrong ! The good answer is B." in result.output
    explication = (
        "The reversing lights of a vehicle are white and indicate to you that the car has engaged reverse gear."
    )

    assert explication in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 1" in result.output


def test_question_command_with_unknown_country() -> None:
    # Given : I have an unknown country
    country = "jp"
    # When : I run question command with country
    with pytest.raises(BadCountryException) as exc_info:
        run_question_command(country=country)
    # Then : Command has raise an exception with good message
    assert "jp is not a valid country (fr,en)" in str(exc_info.value)
