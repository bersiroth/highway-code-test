import unittest
from typing import List, NamedTuple
from unittest.mock import seal

import pytest
from pytest_mock import MockerFixture

from highway_code.domain.model.question import Question
from highway_code.domain.question.exception import (
    BadCountryException,
    EmptyQuestionListException,
)
from highway_code.domain.question.manager import QuestionManager
from highway_code.domain.question.render import (
    CliRenderQuestion,
    CliRenderQuestionManager,
)
from highway_code.domain.translation.translation import TranslationInterface
from tests.unit.factory import question_factory_test


class MocksStruct(NamedTuple):
    question_repository: unittest.mock.Mock
    translation: unittest.mock.Mock
    cli_render_question_manager: unittest.mock.Mock
    cli_render_question: unittest.mock.Mock


def get_mocks(mocker: MockerFixture, questions: List[Question]) -> MocksStruct:
    question_repository_mock = mocker.Mock()
    question_repository_mock.get_all_question.return_value = questions
    seal(question_repository_mock)

    translation_mock = mocker.Mock(spec_set=TranslationInterface)
    translation_mock.load_translation()
    translation_mock.translate.return_value = "translated message"
    seal(translation_mock)

    cli_render_question_manager_mock = mocker.Mock(spec_set=CliRenderQuestionManager)
    seal(cli_render_question_manager_mock)

    cli_render_question_mock = mocker.Mock(spec_set=CliRenderQuestion)
    seal(cli_render_question_mock)

    return MocksStruct(
        question_repository_mock, translation_mock, cli_render_question_manager_mock, cli_render_question_mock
    )


def test_selection_question(mocker: MockerFixture) -> None:
    question = question_factory_test()
    questions = [question]
    mocks = get_mocks(mocker=mocker, questions=questions)

    # Given: I have a valid country
    country = "fr"
    # When: I want select a question
    question_manager = QuestionManager(*mocks)
    selected_question = question_manager.select_question(country=country)
    # Then: I have a good question
    assert question == selected_question
    mocks.question_repository.get_all_question.assert_called_with(country)
    mocks.translation.load_translation.assert_called_with(country)


def test_selection_question_multiple(mocker: MockerFixture) -> None:
    questions = [question_factory_test(), question_factory_test(id=2)]
    mocks = get_mocks(mocker=mocker, questions=questions)

    # Given: I have a valid country
    country = "fr"
    # When: I want select two questions
    question_manager = QuestionManager(*mocks)
    first_selected_question = question_manager.select_question(country=country)
    second_selected_question = question_manager.select_question(country=country)
    # Then: Questions are not same
    assert first_selected_question is not second_selected_question


def test_selection_question_form_id(mocker: MockerFixture) -> None:
    questions = [question_factory_test(id=1), question_factory_test(id=2)]
    mocks = get_mocks(mocker=mocker, questions=questions)

    # Given: I have a valid country and a question id
    country = "fr"
    question_id = 1
    # When: I want select two questions
    question_manager = QuestionManager(*mocks)
    selected_question = question_manager.select_question(country=country, question_id=question_id)
    # Then: Questions are not same
    assert questions[0] == selected_question


def test_selection_question_form_non_existing_id(mocker: MockerFixture) -> None:
    questions = [question_factory_test(id=1)]
    mocks = get_mocks(mocker=mocker, questions=questions)
    cli_render_question_manager_mock = mocker.patch("highway_code.domain.question.render.CliRenderQuestionManager")
    cli_render_question_manager_mock.render_error()
    seal(cli_render_question_manager_mock)
    mocks = mocks._replace(cli_render_question_manager=cli_render_question_manager_mock)

    # Given: I have a valid country and a non-existing question id
    country = "fr"
    non_existing_question_id = 2
    # When: I want select two questions
    question_manager = QuestionManager(*mocks)
    with pytest.raises(SystemExit) as exc_info:
        question_manager.select_question(country=country, question_id=non_existing_question_id)
    # Then: script exit with code 1
    assert SystemExit == exc_info.type
    assert 1 == exc_info.value.code


def test_selection_question_on_unknown_country(mocker: MockerFixture) -> None:
    questions: List[Question] = []
    mocks = get_mocks(mocker=mocker, questions=questions)

    # Given: I have an unknown country
    unknown_country = "jp"
    # When: I want select a question on unknown country
    question_manager = QuestionManager(*mocks)
    with pytest.raises(BadCountryException) as exc_info:
        question_manager.select_question(country=unknown_country)
    # Then: I have an exception with good message
    assert "jp is not a valid country (fr,en)" in str(exc_info.value)


def test_selection_question_on_empty_list(mocker: MockerFixture) -> None:
    questions: List[Question] = []
    mocks = get_mocks(mocker=mocker, questions=questions)

    # When: I want select a question on empty list
    question_manager = QuestionManager(*mocks)
    with pytest.raises(EmptyQuestionListException) as exc_info:
        question_manager.select_question(country="fr")
    # Then: I have an exception with good message
    assert "Impossible to select question on empty question list" in str(exc_info.value)
