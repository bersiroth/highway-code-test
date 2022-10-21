"""
Fixture logic
"""
import os
import shutil
from pathlib import Path


def load_fixture(path: str) -> None:
    """
    Load fixture
    """
    fixture_file = str(Path(__file__).parent) + "/fr/questions.json"
    data_file = path + "/data/fr"
    os.makedirs(data_file)
    shutil.copyfile(fixture_file, data_file + "/questions.json")

    fixture_file = str(Path(__file__).parent) + "/en/questions.json"
    data_file = path + "/data/en"
    os.makedirs(data_file)
    shutil.copyfile(fixture_file, data_file + "/questions.json")

    fixture_file = str(Path(__file__).parent) + "/../locales"
    data_file = path + "/locales"
    shutil.copytree(fixture_file, data_file)
