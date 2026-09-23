def _get_single_key(pat, silent):
    keys = _select_options(pat)
    if len(keys) == 0:
        if not silent:
            _warn_if_deprecated(pat)
        raise OptionError('No such keys(s): %r' % pat)
    if len(keys) > 1:
        raise OptionError('Pattern matched multiple keys')
    key = keys[0]

    if not silent:
        _warn_if_deprecated(key)

    key = _translate_key(key)

    return key
