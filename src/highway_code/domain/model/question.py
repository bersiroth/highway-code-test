"""
Model question
"""
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from typing import List, ClassVar, Tuple


@dataclass(frozen=True)
class Title:
    """
    Title class
    """

    principal: str
    sub: List[str | None]


@dataclass(frozen=True)
class Question:
    """
    Model question
    """

    question_id: int
    title: Title
    propositions: List[str]
    responses: List[str]
    explication: str
    labels: ClassVar[Tuple[str, str, str, str]] = ("A", "B", "C", "D")

    def answer_is_label(self, answer: str) -> bool:
        labels = self.labels[: len(self.propositions)]
        for answer in answer.split(","):
            if answer.upper() not in labels:
                return False
        return True

    def validate_answer(self, answers: str) -> bool:
        for answer in answers.split(","):
            if answer.upper() not in self.responses:
                return False
        return True


class QuestionRepositoryInterface:

    @abstractmethod
    def get_all_question(self, country: str) -> List[Question]:
        pass
