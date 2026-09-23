def is_period(arr):
    """
    Check whether an array-like is a periodical index.

    .. deprecated:: 0.24.0

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

    warnings.warn("'is_period' is deprecated and will be removed in a future "
                  "version.  Use 'is_period_dtype' or is_period_arraylike' "
                  "instead.", FutureWarning, stacklevel=2)

    return isinstance(arr, ABCPeriodIndex) or is_period_arraylike(arr)
