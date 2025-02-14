EN_US = "en_US"
FR_FR = "fr_FR"
ES_ES = "es_ES"
DE_DE = "de_DE"
IT_IT = "it_IT"
PT_PT = "pt_PT"

ALL_LANGUAGES = [
    FR_FR,
    EN_US,
    ES_ES,
    DE_DE,
    IT_IT,
    PT_PT
]

LANGUAGES_TO_DEEPL = {
    FR_FR: 'FR',
    EN_US: 'EN-US',
    ES_ES: 'ES',
    DE_DE: 'DE',
    IT_IT: 'IT',
    PT_PT: 'PT-PT'
}

LOG_FORMAT = '[%(levelname)s] : %(message)s'

PLUGIN_DIRS = ['core', 'desktop', 'plugin_info']
FILE_EXTS = ['.php', '.js', '.json', '.html']

PLUGIN_INFO_JSON = 'plugin_info/info.json'

PLUGIN_ROOT = 'plugin'
CORE_ROOT = 'jeedom_core'
TRANSLATIONS_FILES_PATH = 'core/i18n'

INPUT_SOURCE_LANGUAGE = 'source_language'
INPUT_TARGET_LANGUAGES = 'target_languages'
INPUT_DEEPL_API_KEY = 'deepl_api_key'
INPUT_INCLUDE_EMPTY_TRANSLATION = 'include_empty_translation'
INPUT_USE_CORE_TRANSLATIONS = 'use_core_translations'
INPUT_GENERATE_SOURCE_LANGUAGE_TRANSLATIONS = 'generate_source_language_translations'
INPUT_DEBUG = 'debug'