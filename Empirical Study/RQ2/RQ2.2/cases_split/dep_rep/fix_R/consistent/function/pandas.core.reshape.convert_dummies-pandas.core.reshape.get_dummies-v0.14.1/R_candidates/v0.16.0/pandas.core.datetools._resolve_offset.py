def _resolve_offset(freq, kwds):
    if 'timeRule' in kwds or 'offset' in kwds:
        offset = kwds.get('offset', None)
        offset = kwds.get('timeRule', offset)
        if isinstance(offset, compat.string_types):
            offset = getOffset(offset)
        warn = True
    else:
        offset = freq
        warn = False

    if warn:
        import warnings
        warnings.warn("'timeRule' and 'offset' parameters are deprecated,"
                      " please use 'freq' instead",
                      FutureWarning)

    return offset
