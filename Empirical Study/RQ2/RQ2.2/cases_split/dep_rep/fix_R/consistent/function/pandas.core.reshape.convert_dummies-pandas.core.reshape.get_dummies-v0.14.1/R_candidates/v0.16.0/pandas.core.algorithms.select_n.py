def select_n(series, n, take_last, method):
    """Implement n largest/smallest.

    Parameters
    ----------
    n : int
    take_last : bool
    method : str, {'nlargest', 'nsmallest'}

    Returns
    -------
    nordered : Series
    """
    dtype = series.dtype
    if not issubclass(dtype.type, (np.integer, np.floating, np.datetime64,
                                   np.timedelta64)):
        raise TypeError("Cannot use method %r with dtype %s" % (method, dtype))

    if n <= 0:
        return series[[]]

    dropped = series.dropna()

    if n >= len(series):
        return select_n_slow(dropped, n, take_last, method)

    inds = _select_methods[method](dropped.values, n, take_last)
    return dropped.iloc[inds]
