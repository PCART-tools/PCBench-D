def _is_deprecated(key):
    """ Returns True if the given option has been deprecated """

    key = key.lower()
    return key in _deprecated_options
