@functools.lru_cache()
def get_languages():
    """
    Cache of settings.LANGUAGES in a dictionary for easy lookups by key.
    """
    return dict(settings.LANGUAGES)
