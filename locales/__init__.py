from locales import ru, uz, en

LOCALES = {
    "ru": ru.TEXTS,
    "uz": uz.TEXTS,
    "en": en.TEXTS,
}

DEFAULT_LANG = "ru"
SUPPORTED_LANGS = ["ru", "uz", "en"]


def t(lang: str, key: str, **kwargs) -> str:
    """Get a translated string by key, formatted with kwargs."""
    lang = lang if lang in LOCALES else DEFAULT_LANG
    texts = LOCALES[lang]
    template = texts.get(key) or LOCALES[DEFAULT_LANG].get(key) or key
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template
