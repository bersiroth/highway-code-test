"""Render statistic"""
from __future__ import annotations

import sys
from dataclasses import dataclass

from highway_code.domain.question.manager import QuestionManager
from highway_code.domain.statistic.manager import StatisticManager


@dataclass(frozen=True)
class StatisticCommand:
    """Command for render statistic"""

    reset: bool


class StatisticHandler:
    """Handler answer command"""

    __statisticManager: StatisticManager

    def __init__(self, statistic_manager: StatisticManager):
        self.__statisticManager = statistic_manager

    def handle(self, command: StatisticCommand) -> None:
        if command.reset:
            self.__statisticManager.reset()

        self.__statisticManager.show_statistic()
