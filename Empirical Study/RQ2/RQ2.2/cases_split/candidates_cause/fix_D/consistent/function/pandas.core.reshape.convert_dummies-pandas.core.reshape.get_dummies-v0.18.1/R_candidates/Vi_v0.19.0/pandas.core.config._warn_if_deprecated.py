def _warn_if_deprecated(key):
    """
    Checks if `key` is a deprecated option and if so, prints a warning.

    Returns
    -------
    bool - True if `key` is deprecated, False otherwise.
    """

    d = _get_deprecated_option(key)
    if d:
        if d.msg:
            print(d.msg)
            warnings.warn(d.msg, DeprecationWarning)
        else:
            msg = "'%s' is deprecated" % key
            if d.removal_ver:
                msg += ' and will be removed in %s' % d.removal_ver
            if d.rkey:
                msg += ", please use '%s' instead." % d.rkey
            else:
                msg += ', please refrain from using it.'

            warnings.warn(msg, DeprecationWarning)
        return True
    return False
