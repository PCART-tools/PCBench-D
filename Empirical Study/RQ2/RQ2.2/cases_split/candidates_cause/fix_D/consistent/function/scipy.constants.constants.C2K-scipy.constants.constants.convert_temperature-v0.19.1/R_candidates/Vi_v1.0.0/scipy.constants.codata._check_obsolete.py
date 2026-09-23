def _check_obsolete(key):
    if key in _obsolete_constants and key not in _aliases:
        warnings.warn("Constant '%s' is not in current %s data set" % (
            key, _current_codata), ConstantWarning)
