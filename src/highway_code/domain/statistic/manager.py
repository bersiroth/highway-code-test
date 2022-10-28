"""
Statistic manager
"""
from highway_code.domain.model.statistic import Statistic, StatisticRepositoryInterface
from highway_code.domain.statistic.render import CliRenderStatistic


class StatisticManager:

    __session: Statistic
    __global: Statistic
    __statistic_repository: StatisticRepositoryInterface
    __cli_render_statistic: CliRenderStatistic

    def __init__(
        self, statistic_repository: StatisticRepositoryInterface, cli_render_statistic: CliRenderStatistic
    ) -> None:
        self.__cli_render_statistic = cli_render_statistic
        self.__statistic_repository = statistic_repository
        self.__global = self.__statistic_repository.load()
        self.__session = Statistic()

    def add_answer(self, is_correct: bool) -> None:
        self.__session.add_answer(is_correct)
        self.__global.add_answer(is_correct)

    def show_statistic(self) -> None:
        self.__cli_render_statistic.render_all_statistics(self.__global, self.__session)

    def save(self):
        self.__statistic_repository.save(self.__global)

    def reset(self):
        self.__global = Statistic()
        self.__statistic_repository.save(self.__global)
