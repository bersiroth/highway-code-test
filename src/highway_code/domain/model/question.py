from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Title:
    principal: str
    sub: List[str]


@dataclass(frozen=True)
class Question:
    question_id: int
    title: Title
    propositions: List[str]
    responses: List[str]
    explication: str
    labels: Tuple[str, str, str, str] = ("A", "B", "C", "D")

    def answer_is_label(self, answers: str) -> bool:
        labels = self.labels[: len(self.propositions)]
        for answer in answers.split(","):
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
