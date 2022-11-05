"""
Statistic manager
"""
from highway_code.domain.model.statistic import Statistic, StatisticRepositoryInterface
from highway_code.domain.statistic.render import CliRenderStatistic


class StatisticManager:
    def __init__(
        self, statistic_repository: StatisticRepositoryInterface, cli_render_statistic: CliRenderStatistic
    ) -> None:
        self.cli_render_statistic = cli_render_statistic
        self.statistic_repository = statistic_repository
        self.stat_global = self.statistic_repository.load()
        self.stat_session = Statistic()

    def add_answer(self, is_correct: bool) -> None:
        self.stat_session.add_answer(is_correct)
        self.stat_global.add_answer(is_correct)

    def show_statistic(self) -> None:
        self.cli_render_statistic.render_all_statistics(self.stat_global, self.stat_session)

    def save(self) -> None:
        self.statistic_repository.save(self.stat_global)

    def reset(self) -> None:
        self.stat_global = Statistic()
        self.statistic_repository.save(self.stat_global)
