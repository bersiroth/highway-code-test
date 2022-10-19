import os
from pathlib import Path
from typing import List


class Fixture_Manager:

    file_list = [
        'questions.json',
    ]

    def get(self) -> List[str]:
        fixture = []
        for file in self.file_list:
            with open(f"{Path(__file__).parent}/{file}", "r") as f:
                fixture.append(f.read())
        return fixture

    def write(self, fixture: List[str]) -> None:
        os.mkdir("data")
        for key, file in enumerate(self.file_list):
            with open(f"data/{file}", "w+") as f:
                f.write(fixture[key])

