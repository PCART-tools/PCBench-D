def all_locale_paths():
    """
    Return a list of paths to user-provides languages files.
    """
    globalpath = os.path.join(
        os.path.dirname(sys.modules[settings.__module__].__file__), 'locale')
    return [globalpath] + list(settings.LOCALE_PATHS)
