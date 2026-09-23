@functools.lru_cache()
def get_languages():
    """
    Cache of settings.LANGUAGES in an OrderedDict for easy lookups by key.
    """
    return OrderedDict(settings.LANGUAGES)
