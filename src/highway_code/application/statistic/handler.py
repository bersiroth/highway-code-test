from __future__ import annotations

from dataclasses import dataclass

from highway_code.domain.statistic.manager import StatisticManager


@dataclass(frozen=True)
class StatisticCommand:
    reset: bool


class StatisticHandler:
    def __init__(self, statistic_manager: StatisticManager):
        self.statisticManager = statistic_manager

    def handle(self, command: StatisticCommand) -> None:
        if command.reset:
            self.statisticManager.reset()

        self.statisticManager.show_statistic()
