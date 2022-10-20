"""
Fixture logic
"""
import os
from pathlib import Path
from typing import List


class FixtureManager:
    """
    Fixture manager
    """

    file_list = [
        "questions.json",
    ]

    def get(self) -> List[str]:
        """
        Get fixture from json file
        """
        fixture = []
        for file in self.file_list:
            with open(f"{Path(__file__).parent}/{file}", "r", encoding="utf-8") as fixture_file:
                fixture.append(fixture_file.read())
        return fixture

    def load(self, fixture: List[str]) -> None:
        """
        Load fixture
        """
        os.mkdir("data")
        for key, file in enumerate(self.file_list):
            with open(f"data/{file}", "w+", encoding="utf-8") as fixture_file:
                fixture_file.write(fixture[key])
