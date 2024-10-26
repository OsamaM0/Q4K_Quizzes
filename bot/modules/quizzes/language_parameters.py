from bot.modules.database.mongodb import MongoDB
from bot.modules.translator import LANG_CODE_LIST
class LangMSG:
    # Default language if none is set
    global_context_store = {}
    # # Cache to store loaded translations
    # _translation_cache = {}

    # @staticmethod
    # def _load_translations(lang_code):
    #     """
    #     Load the translation JSON file for the given language code.
    #     Cache it for future access.
    #     """
    #     if lang_code not in LangMSG._translation_cache:
    #         try:
    #             # Load the JSON file from the translations directory
    #             with open(f'bot/translations/{lang_code}.json', 'r', encoding='utf-8') as f:
    #                 LangMSG._translation_cache[lang_code] = json.load(f)
    #         except FileNotFoundError:
    #             # Fallback to the default language if file not found
    #             if lang_code != LangMSG.DEFAULT_LANGUAGE:
    #                 return LangMSG._load_translations(LangMSG.DEFAULT_LANGUAGE)
    #             else:
    #                 raise ValueError(f"Translation file for '{lang_code}' not found.")
    #     return LangMSG._translation_cache[lang_code]

    @staticmethod
    async def get_language(user_id):
        """
        Get the user's preferred language from context.user_data.
        If not set, return the default language (set globally or passed as an argument).
        """
        if user_id not in LangMSG.global_context_store:
            language_code = await MongoDB.find_one("users", "user_id", user_id)
            if not language_code:
                language_code = "en"
            else:
                language_code = language_code.get("lang")
            await LangMSG.set_language(user_id, language_code)

        print(LangMSG.global_context_store)
        return LangMSG.global_context_store.get(user_id, "en")

    @staticmethod
    async def set_language(user_id, language_code=None):
        """
        Set the user's language in context.user_data.
        Perform basic validation to ensure it's a valid ISO 639-1 code (e.g., 'en', 'es', etc.).
        """
        if not language_code:
            language_code = await MongoDB.find_one("users", "user_id", user_id)
            language_code = language_code.get("lang")
            await LangMSG.set_language(user_id, language_code)
            
        elif language_code in LANG_CODE_LIST:
            LangMSG.global_context_store[user_id] = language_code
        else:
            raise ValueError(
                "Invalid language code. Must be a 2-character ISO 639-1 code.")

    # @staticmethod
    # def translate(context, key):
    #     """
    #     Translate a given key using the user's preferred language.
    #     Load the translation from JSON if not cached.
    #     """
    #     user_lang = LangMSG.get_language(context)
    #     translations = LangMSG._load_translations(user_lang)
    #     # Fallback to the default language if the key isn't found
    #     return translations.get(key, LangMSG._load_translations(LangMSG.DEFAULT_LANGUAGE).get(key, key))

    # @staticmethod
    # def reset_language(context):
    #     """
    #     Reset the user's language to the default language.
    #     """
    #     context.user_data['language_code'] = LangMSG.DEFAULT_LANGUAGE
