@_logged_cached('CACHEDIR=%s')
def get_cachedir():
    """
    Return the string path of the cache directory.

    The procedure used to find the directory is the same as for
    _get_config_dir, except using ``$XDG_CACHE_HOME``/``$HOME/.cache`` instead.
    """
    return _get_config_or_cache_dir(_get_xdg_cache_dir)
