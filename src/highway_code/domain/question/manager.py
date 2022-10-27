"""
Question manager
"""
from __future__ import annotations

import sys
import random
from typing import List, Dict

from typing_extensions import TypeGuard

from highway_code.domain.model.question import Question, QuestionRepositoryInterface
from highway_code.domain.question.render import CliRenderQuestionManager, CliRenderQuestion
from highway_code.domain.translation.translation import TranslationInterface


class QuestionManager:
    """
    Model question
    """

    # TODO: why dict and not directly list of Question move to question model
    __questions_list: Dict[str, List[Question]] = {}
    __translation: TranslationInterface
    __cli_render_question: CliRenderQuestion
    __cli_render_question_manager: CliRenderQuestionManager
    __question_repository: QuestionRepositoryInterface

    def __init__(
        self,
        question_repository: QuestionRepositoryInterface,
        translation: TranslationInterface,
        cli_render_question_manager: CliRenderQuestionManager,
        cli_render_question: CliRenderQuestion
    ):
        debug(self.__questions_list)
        self.__question_repository = question_repository
        self.__translation = translation
        self.__cli_render_question = cli_render_question
        self.__cli_render_question_manager = cli_render_question_manager

    def select_question(self, country: str, question_id: int | None) -> Question:
        """
        Select question
        """
        if country not in self.__questions_list:
            debug(self.__questions_list)
            self.__questions_list[country] = self.__question_repository.get_all_question(country)

        self.__translation.load_translation(country)
        if question_id is not None:
            def question_filter(current_question: Question) -> TypeGuard[Question | None]:
                return current_question.question_id == question_id
            question = next(filter(question_filter, self.__questions_list[country]), None)
            if question is None:
                message = self.__translation.translate("Question id {id} not found.").format(id=question_id)
                self.__cli_render_question_manager.render_error(message)
                sys.exit(1)
            return question

        system_random = random.SystemRandom()
        questions_list = self.__questions_list[country]
        rand_int = system_random.randint(0, len(questions_list) - 1)
        question = questions_list[rand_int]
        questions_list.remove(question)
        return question

    def question_list_is_empty(self, country: str) -> bool:
        """
        Check if list is empty
        """
        return len(self.__questions_list[country]) == 0

    def process_question(self, question: Question) -> bool:
        self.__cli_render_question.show_question(question)
        while True:
            message = self.__translation.translate("Enter your answer with label letter separated by comma. (Ex: A,C)")
            answer = self.__cli_render_question_manager.ask_answer(message)
            if question.answer_is_label(answer):
                break
            labels = question.labels[: len(question.propositions)]
            message = self.__translation.translate(
                "ERROR: {answer} is not in labels ({labels}), try again."
            ).format(answer=answer, labels=",".join(labels))
            self.__cli_render_question_manager.render_error(message)

        is_correct_answer = question.validate_answer(answer)
        if is_correct_answer:
            message = self.__translation.translate("Correct !")
            self.__cli_render_question.render_correction(question, message, is_correct_answer)
        else:
            responses = ",".join(question.responses).lower()
            message = self.__translation.translate("Wrong ! The good answer is {responses}.").format(
                responses=responses.upper()
            )
            self.__cli_render_question.render_correction(question, message, is_correct_answer)
        return is_correct_answer

    def ask_question_again(self) -> bool:
        message = self.__translation.translate("New question ?")
        return self.__cli_render_question_manager.ask_question_again(message)

    def show_congratulation(self):
        message = self.__translation.translate("Congratulation ! You have answer to all questions")
        return self.__cli_render_question_manager.show_congratulation(message)

