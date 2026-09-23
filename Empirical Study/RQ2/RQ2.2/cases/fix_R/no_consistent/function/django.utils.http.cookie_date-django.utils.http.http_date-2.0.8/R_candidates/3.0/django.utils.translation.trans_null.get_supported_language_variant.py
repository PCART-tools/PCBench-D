def get_supported_language_variant(lang_code, strict=False):
    if lang_code == settings.LANGUAGE_CODE:
        return lang_code
    else:
        raise LookupError(lang_code)
