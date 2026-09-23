def match(to_match, values, na_sentinel=-1):
    """
    Compute locations of to_match into values

    Parameters
    ----------
    to_match : array-like
        values to find positions of
    values : array-like
        Unique set of values
    na_sentinel : int, default -1
        Value to mark "not found"

    Examples
    --------

    Returns
    -------
    match : ndarray of integers
    """
    values = com._asarray_tuplesafe(values)
    if issubclass(values.dtype.type, string_types):
        values = np.array(values, dtype='O')

    f = lambda htype, caster: _match_generic(to_match, values, htype, caster)
    result = _hashtable_algo(f, values.dtype, np.int64)

    if na_sentinel != -1:

        # replace but return a numpy array
        # use a Series because it handles dtype conversions properly
        from pandas.core.series import Series
        result = Series(result.ravel()).replace(-1, na_sentinel).values.\
            reshape(result.shape)

    return result
