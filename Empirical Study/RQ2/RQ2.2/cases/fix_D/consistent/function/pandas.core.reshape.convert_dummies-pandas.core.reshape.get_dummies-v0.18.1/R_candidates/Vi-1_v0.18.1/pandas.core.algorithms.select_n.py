def select_n(series, n, keep, method):
    """Implement n largest/smallest.

    Parameters
    ----------
    n : int
    keep : {'first', 'last'}, default 'first'
    method : str, {'nlargest', 'nsmallest'}

    Returns
    -------
    nordered : Series
    """
    dtype = series.dtype
    if not issubclass(dtype.type, (np.integer, np.floating, np.datetime64,
                                   np.timedelta64)):
        raise TypeError("Cannot use method %r with dtype %s" % (method, dtype))

    if keep not in ('first', 'last'):
        raise ValueError('keep must be either "first", "last"')

    if n <= 0:
        return series[[]]

    dropped = series.dropna()

    if n >= len(series):
        return select_n_slow(dropped, n, keep, method)

    inds = _select_methods[method](dropped.values, n, keep)
    return dropped.iloc[inds]
