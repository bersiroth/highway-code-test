import gettext

from highway_code.domain.translation.translation import TranslationInterface


class GettextTranslation(TranslationInterface):
    def __init__(self, country: str = "en") -> None:
        self.translation = gettext.translation("main", localedir="locales", languages=[country])

    def translate(self, message: str) -> str:
        return self.translation.gettext(message)

    def load_translation(self, country: str) -> None:
        translation = gettext.translation("main", localedir="locales", languages=[country])
        self.translation = translation
