import json
import os
from pathlib import Path

from source_file import SourceFile
from prompt import Prompt
from consts import LANGUAGES, PLUGIN_DIRS, PLUGIN_INFO_JSON
from jeedom_core_translations import JeedomCoreTranslations
from translations import Translations

class TranslatePlugin():

    def __init__(self) -> None:
        self._plugin_root = Path.cwd()
        self._plugin_id: str
        self._plugin_name: str

        self._files: dict[str, SourceFile] = {}
        self._previous_translations = Translations()

        self._jeedom_core_translations = JeedomCoreTranslations()

        self.__read_info_json()
        self._jeedom_core_translations.parse()

    def start(self):
        self.get_previous_translations()
        self.find_prompts_in_all_files()
        self.do_translate()

        self.write_translations()

    def __read_info_json(self):
        info_json = self._plugin_root/PLUGIN_INFO_JSON
        if not info_json.is_file():
            raise RuntimeError("Missing info.json file")

        data = json.loads(info_json.read_text(encoding="UTF-8"))
        self._plugin_id = data['id']
        self._plugin_name = data['name']

    def find_prompts_in_all_files(self):
        print("Find prompts in all plugin files")
        for dir in PLUGIN_DIRS:
            plugin_dir = self._plugin_root/dir
            for root, dirs, files in plugin_dir.walk():
                for dirname in dirs:
                    if root.name == "core" and dirname == 'i18n':
                        dirs.remove(dirname)
                    # for d in excludes:
                    #     if fnmatch.fnmatch(dirname, d):
                    #         dirs.remove(dirname)

                for fileName in files:
                    # for f in excludes:
                    #     if fnmatch.fnmatch(fileName, f):
                    #         continue
                    if fileName[-4:] == ".php" or fileName[-3:] == ".js":
                    #   or fileName[-5:] == ".json"
                    #   or fileName[-5:] == ".html"):
                        absolute_file_path = root/fileName
                        jeedom_file_path = absolute_file_path.relative_to(self._plugin_root)
                        jeedom_file_path = (f"plugins/{self._plugin_id}"/jeedom_file_path).as_posix()
                        print(f"    {jeedom_file_path}...")
                        self._files[jeedom_file_path] = SourceFile(absolute_file_path)
                        self._files[jeedom_file_path].search_prompts()

    def do_translate(self):
        for file in self._files.values():
            for prompt in file.get_prompts().values():
                if prompt.getText() in self._previous_translations:
                    prompt.setTranslations(self._previous_translations.getTranslations(prompt.getText()))
                elif prompt.getText() in self._jeedom_core_translations.getTranslations():
                    prompt.setTranslation(self._jeedom_core_translations.getTranslations().getTranslations(prompt.getText()))


    def get_previous_translations(self):
        print("Read existing translations file...")
        for language in LANGUAGES:
            language_file = self.get_language_file(language)
            if not language_file.exists():
                continue
            try:
                data = json.loads(language_file.read_text(encoding="UTF-8"))
            except OSError as e:
                print(e.filename + ": " + e.strerror)
                return False
            except json.decoder.JSONDecodeError as e:
                print(f"Erreur lors de la lecture du fichier {language_file}:")
                print(f"   Ligne {e.lineno}")
                print(f"   position {e.colno}")
                print(f"   {e.msg}")
                print()
                return False

            for path in data:
                for text in data[path]:
                    self._previous_translations.add_translation(language, text, data[path][text])
        return True

    def get_language_file(self, language: str):
        return self._plugin_root/f"core/i18n/{language}.json"

    def write_translations(self, textes ="" ):
        print("Ecriture du/des fichier(s) de traduction(s)...")
        for language in LANGUAGES:
            print(f"    Language: {language}...")

            translation_path = self._plugin_root/"core/i18n"
            translation_path.mkdir(parents=True, exist_ok=True)
            translation_file = translation_path/f"{language}.json"

            result = {}
            for path, file in self._files.items():
                result[path] = file.get_prompts_and_translation(language)

            print(f"Will dump {translation_file.as_posix()}")
            translation_file.write_text(json.dumps(result, ensure_ascii=False, sort_keys = True, indent= 4).replace("/","\/"), encoding="UTF-8")

if __name__ == "__main__":
    TranslatePlugin().start()