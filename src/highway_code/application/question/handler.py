from __future__ import annotations

import sys
from dataclasses import dataclass

from highway_code.domain.question.manager import QuestionManager
from highway_code.domain.statistic.manager import StatisticManager


@dataclass(frozen=True)
class QuestionCommand:
    question_id: int | None = None
    country: str = "fr"
    error_on_failure: bool = False


class QuestionHandler:
    def __init__(self, question_manager: QuestionManager, statistic_manager: StatisticManager):
        self.statistic_manager = statistic_manager
        self.question_manager = question_manager

    def handle(self, command: QuestionCommand) -> None:
        new_question = True
        is_correct_answer = False

        while new_question:
            question = self.question_manager.select_question(command.country, command.question_id)
            is_correct_answer = self.question_manager.process_question(question)
            self.statistic_manager.add_answer(is_correct_answer)
            if not is_correct_answer and command.error_on_failure:
                break
            if command.question_id is not None:
                break
            if self.question_manager.question_list_is_empty(command.country):
                break
            new_question = self.question_manager.ask_question_again()

        if self.question_manager.question_list_is_empty(command.country):
            self.question_manager.show_congratulation()
        self.statistic_manager.show_statistic()
        self.statistic_manager.save()

        if not is_correct_answer and command.error_on_failure:
            sys.exit(1)
