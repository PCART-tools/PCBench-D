def is_period(arr):
    """
    Check whether an array-like is a periodical index.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean : Whether or not the array-like is a periodical index.

    Examples
    --------
    >>> is_period([1, 2, 3])
    False
    >>> is_period(pd.Index([1, 2, 3]))
    False
    >>> is_period(pd.PeriodIndex(["2017-01-01"], freq="D"))
    True
    """

    # TODO: do we need this function?
    # It seems like a repeat of is_period_arraylike.
    return isinstance(arr, ABCPeriodIndex) or is_period_arraylike(arr)
