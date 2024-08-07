class Prompt():

    def __init__(self, text) -> None:
        self._text: str = text
        self._translations: dict[str, str] = {}

    def getText(self):
        return self._text

    def hasTranslation(self, language: str):
        return language in self._translations

    def setTranslation(self, language: str, translation: str):
        self._translations[language] = translation

    def getTranslation(self, language: str):
        return self._translations[language] if language in self._translations else None

    def setTranslations(self, translations: dict[str, str]):
        self._translations = translations

    def getTranslations(self):
        return self._translations
