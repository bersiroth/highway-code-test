from unittest.mock import seal

from pytest_mock import MockerFixture

from highway_code.application.question.handler import QuestionCommand, QuestionHandler
from tests.unit.factory import question_factory_test


def test_question_handler(mocker: MockerFixture) -> None:
    question_manager_mock = mocker.patch("highway_code.domain.question.manager.QuestionManager")
    question = question_factory_test()
    question_manager_mock.select_question.return_value = question
    question_manager_mock.process_question.return_value = True
    question_manager_mock.question_list_is_empty.return_value = False
    question_manager_mock.ask_question_again.return_value = False
    seal(question_manager_mock)
    statistic_manager_mock = mocker.patch("highway_code.domain.statistic.manager.StatisticManager")
    statistic_manager_mock.add_answer()
    statistic_manager_mock.show_statistic()
    statistic_manager_mock.save()
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
