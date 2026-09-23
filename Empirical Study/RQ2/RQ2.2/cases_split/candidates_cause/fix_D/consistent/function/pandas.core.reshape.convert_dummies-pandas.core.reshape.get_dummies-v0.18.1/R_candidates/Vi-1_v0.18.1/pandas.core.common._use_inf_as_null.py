def _use_inf_as_null(key):
    """Option change callback for null/inf behaviour
    Choose which replacement for numpy.isnan / -numpy.isfinite is used.

    Parameters
    ----------
    flag: bool
        True means treat None, NaN, INF, -INF as null (old way),
        False means None and NaN are null, but INF, -INF are not null
        (new way).

    Notes
    -----
    This approach to setting global module values is discussed and
    approved here:

    * http://stackoverflow.com/questions/4859217/
      programmatically-creating-variables-in-python/4859312#4859312
    """
    flag = get_option(key)
    if flag:
        globals()['_isnull'] = _isnull_old
    else:
        globals()['_isnull'] = _isnull_new
