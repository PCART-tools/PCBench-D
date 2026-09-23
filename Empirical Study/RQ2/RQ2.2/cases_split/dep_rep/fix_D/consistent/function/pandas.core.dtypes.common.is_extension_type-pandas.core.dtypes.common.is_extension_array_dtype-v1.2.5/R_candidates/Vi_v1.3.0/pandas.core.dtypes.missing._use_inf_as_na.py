def _use_inf_as_na(key):
    """
    Option change callback for na/inf behaviour.

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

    * https://stackoverflow.com/questions/4859217/
      programmatically-creating-variables-in-python/4859312#4859312
    """
    inf_as_na = get_option(key)
    globals()["_isna"] = partial(_isna, inf_as_na=inf_as_na)
    if inf_as_na:
        globals()["nan_checker"] = lambda x: ~np.isfinite(x)
        globals()["INF_AS_NA"] = True
    else:
        globals()["nan_checker"] = np.isnan
        globals()["INF_AS_NA"] = False
