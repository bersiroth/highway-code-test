"""
Gettext Translation
"""
import gettext

from highway_code.domain.translation.translation import TranslationInterface


class GettextTranslation(TranslationInterface):

    __translation: gettext.NullTranslations

    def translate(self, message: str) -> str:
        return self.__translation.gettext(message)

    def load_translation(self, country: str) -> None:
        translation = gettext.translation("main", localedir="locales", languages=[country])
        self.__translation = translation

