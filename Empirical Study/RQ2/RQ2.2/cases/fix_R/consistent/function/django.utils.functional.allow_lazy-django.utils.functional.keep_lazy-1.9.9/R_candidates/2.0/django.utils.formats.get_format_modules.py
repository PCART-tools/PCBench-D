def get_format_modules(lang=None, reverse=False):
    """Return a list of the format modules found."""
    if lang is None:
        lang = get_language()
    if lang not in _format_modules_cache:
        _format_modules_cache[lang] = list(iter_format_modules(lang, settings.FORMAT_MODULE_PATH))
    modules = _format_modules_cache[lang]
    if reverse:
        return list(reversed(modules))
    return modules
