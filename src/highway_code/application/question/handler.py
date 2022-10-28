"""Answer to a question action"""
from __future__ import annotations

import sys
from dataclasses import dataclass

from highway_code.domain.question.manager import QuestionManager
from highway_code.domain.statistic.manager import StatisticManager


@dataclass(frozen=True)
class QuestionCommand:
    """Command for answer to a question"""

    question_id: int | None
    country: str
    error_on_failure: bool


class QuestionHandler:
    """Handler answer command"""

    __question_manager: QuestionManager
    __statisticManager: StatisticManager

    def __init__(self, question_manager: QuestionManager, statistic_manager: StatisticManager):
        self.__statisticManager = statistic_manager
        self.__question_manager = question_manager

    def handle(self, command: QuestionCommand) -> None:
        new_question = True
        is_correct_answer = False

        while new_question:
            question = self.__question_manager.select_question(command.country, command.question_id)
            is_correct_answer = self.__question_manager.process_question(question)
            self.__statisticManager.add_answer(is_correct_answer)
            if not is_correct_answer and command.error_on_failure:
                break
            if command.question_id is not None:
                break
            if self.__question_manager.question_list_is_empty(command.country):
                break
            new_question = self.__question_manager.ask_question_again()

        if self.__question_manager.question_list_is_empty(command.country):
            self.__question_manager.show_congratulation()
        self.__statisticManager.show_statistic()
        self.__statisticManager.save()

        if not is_correct_answer and command.error_on_failure:
            sys.exit(1)
