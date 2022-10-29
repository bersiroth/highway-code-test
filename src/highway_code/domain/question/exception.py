from typing import List


class BadCountryException(Exception):
    @staticmethod
    def from_country_and_available_countries(country: str, available_countries: List[str]):
        return BadCountryException(f'{country} is not a valid country ({",".join(available_countries) })')


class EmptyQuestionListException(Exception):
    def __init__(self):
        super().__init__("Impossible to select question on empty question list")
