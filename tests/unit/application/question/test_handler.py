from unittest.mock import seal

import pytest
from pytest_mock import MockerFixture

from highway_code.application.question.handler import QuestionCommand, QuestionHandler
from highway_code.domain.model.question import Question, Title
from highway_code.domain.question.exception import BadCountry


def test_question_handler(mocker: MockerFixture) -> None:
    question_manager_mock = mocker.patch("highway_code.domain.question.manager.QuestionManager")
    question = Question(1, Title("title", []), ["oui", "non"], ["A"], "explication")
    question_manager_mock.select_question.return_value = question
    question_manager_mock.process_question.return_value = True
    question_manager_mock.question_list_is_empty.return_value = False
    question_manager_mock.ask_question_again.return_value = False
    statistic_manager_mock = mocker.patch("highway_code.domain.statistic.manager.StatisticManager")
    statistic_manager_mock.add_answer()
    statistic_manager_mock.show_statistic()
    statistic_manager_mock.save()
    seal(question_manager_mock)
    seal(statistic_manager_mock)

    # Given: I have a Question Command
    command = QuestionCommand(country="fr")
    # When: I handle this command
    handler = QuestionHandler(question_manager_mock, statistic_manager_mock)
    handler.handle(command)
    # Then: Question is selected and processed by manager and result has added to statistic
    question_manager_mock.select_question.assert_called_with("fr", None)
    question_manager_mock.process_question.assert_called_with(question)
    question_manager_mock.question_list_is_empty.assert_called_with("fr")
    statistic_manager_mock.add_answer.assert_called_with(True)


def test_question_handler_with_unknown_country(mocker: MockerFixture) -> None:
    question_manager_mock = mocker.patch("highway_code.domain.question.manager.QuestionManager")
    question_manager_mock.select_question.side_effect = BadCountry("jp is not a valid country (fr,en))")
    statistic_manager_mock = mocker.patch("highway_code.domain.statistic.manager.StatisticManager")
    seal(question_manager_mock)
    seal(statistic_manager_mock)

    # Given: I have a Question Command with an unknown country
    command = QuestionCommand(country="jp")
    # When: I handle this command
    with pytest.raises(BadCountry) as exc_info:
        handler = QuestionHandler(question_manager_mock, statistic_manager_mock)
        handler.handle(command)
    # Then : An exception has raised with good message
    assert "jp is not a valid country (fr,en)" in str(exc_info.value)
