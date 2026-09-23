def get_default_val(pat):
    key = _get_single_key(pat, silent=True)
    return _get_registered_option(key).defval
