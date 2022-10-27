"""
Model question
"""
from __future__ import annotations

from abc import abstractmethod
from datetime import date


class Statistic:
    """
    Model statistic
    """

    __answer: int
    __correct: int
    __wrong: int
    __last: str

    def __init__(self, answer: int = 0, correct: int = 0, wrong: int = 0, last: str = "1999-01-01"):
        self.__answer = answer
        self.__correct = correct
        self.__wrong = wrong
        self.__last = last

    def add_answer(self, is_correct: bool):
        self.__answer += 1
        if is_correct:
            self.__correct += 1
        else:
            self.__wrong += 1
        self.__last = date.today().isoformat()

    def is_empty(self) -> bool:
        return self.__answer == 0

    @property
    def answer(self) -> int:
        return self.__answer

    @property
    def correct(self) -> int:
        return self.__correct

    @property
    def wrong(self) -> int:
        return self.__wrong

    @property
    def last(self) -> str:
        return self.__last


class StatisticRepositoryInterface:

    @abstractmethod
    def load(self) -> Statistic:
        pass

    @abstractmethod
    def save(self, statistic: Statistic) -> None:
        pass
