"""
Translation logic
"""

from __future__ import annotations

import gettext


class Translation:
    """
    Translation class
    """

    __country: str
    __translation: gettext.NullTranslations

    def __init__(self, country: str):
        self.__country = country
        translation = gettext.translation("main", localedir="locales", languages=[self.__country])
        translation.install("gettext")
        self.__translation = translation

    def translate(self, message) -> str:
        """
        Translate message
        """
        return self.__translation.gettext(message)

    @property
    def country(self) -> str:
        """
        Get country
        """
        return self.__country
