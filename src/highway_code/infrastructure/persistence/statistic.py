import json
from os.path import exists

from highway_code.domain.model.statistic import Statistic, StatisticRepositoryInterface


class JsonStatisticRepository(StatisticRepositoryInterface):
    def load(self) -> Statistic:
        file = "data/stats.json"
        if not exists(file):
            return Statistic()
        with open(file, "r", encoding="utf-8") as openfile:
            json_data = json.load(openfile)
            return Statistic(json_data["answer"], json_data["correct"], json_data["wrong"], json_data["last"])

    def save(self, statistic: Statistic) -> None:
        with open("data/stats.json", "w+", encoding="utf-8") as openfile:
            json_statistic = json.dumps(
                {
                    "answer": statistic.answer,
                    "correct": statistic.correct,
                    "wrong": statistic.wrong,
                    "last": statistic.last,
                }
            )
            openfile.write(json_statistic)
