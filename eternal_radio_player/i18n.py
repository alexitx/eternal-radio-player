import json
import locale as locale_
import logging

from .constants import LOCALES, DEFAULT_LOCALE, DEFAULT_SYSTEM_LOCALES
from .exceptions import I18nError, ResourceError
from .utils import qt_resource


log = logging.getLogger('i18n')


class I18n:

    locale = DEFAULT_LOCALE
    default_locale = DEFAULT_LOCALE
    fallback = True
    _ts_dict = {}

    @classmethod
    def translate(cls, key, *args, **kwargs):
        raw_msg = cls._ts_dict.get(cls.locale, {}).get(key)
        if raw_msg is None and cls.fallback:
            log.warning(
                f"Translation key '{key}' not found for locale '{cls.locale}', "
                f"falling back to '{cls.default_locale}'"
            )
            raw_msg = cls._ts_dict.get(cls.default_locale, {}).get(key)
        if raw_msg is not None:
            return raw_msg.format(*args, **kwargs)
        raise I18nError(f"No translation found for key '{key}'")

    @classmethod
    def get_language_name(cls, locale):
        lang_name = cls._ts_dict.get(locale, {}).get('language_name')
        if lang_name is None:
            raise I18nError(f"Could not get language name for locale '{locale}'")
        return lang_name

    @classmethod
    def load_translations(cls):
        for locale in LOCALES:
            log.debug(f'Loading translation for locale: {locale}')
            try:
                cls._ts_dict[locale] = json.loads(qt_resource(f':i18n/{locale}.json', True))
            except (ResourceError, json.JSONDecodeError) as e:
                raise I18nError(f"Could not read file for locale '{locale}': {e}") from e

    @classmethod
    def remove_translation(cls, locale):
        if locale in cls._ts_dict:
            log.debug(f'Removing translation for locale: {locale}')
            del cls._ts_dict[locale]

    @staticmethod
    def get_preferred_locale():
        system_locale = locale_.getdefaultlocale()[0]
        for preferred_locale, system_locales in DEFAULT_SYSTEM_LOCALES.items():
            if system_locale in system_locales:
                log.debug(f'Preferred locale: {preferred_locale}')
                return preferred_locale
        log.debug(f'Preferred locale (default): {DEFAULT_LOCALE}')
        return DEFAULT_LOCALE
