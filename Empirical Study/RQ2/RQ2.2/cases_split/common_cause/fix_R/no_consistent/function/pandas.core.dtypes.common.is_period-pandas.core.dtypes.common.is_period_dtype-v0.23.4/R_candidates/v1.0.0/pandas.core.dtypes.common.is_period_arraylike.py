def is_period_arraylike(arr) -> bool:
    """
    Check whether an array-like is a periodical array-like or PeriodIndex.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean
        Whether or not the array-like is a periodical array-like or
        PeriodIndex instance.

    Examples
    --------
    >>> is_period_arraylike([1, 2, 3])
    False
    >>> is_period_arraylike(pd.Index([1, 2, 3]))
    False
    >>> is_period_arraylike(pd.PeriodIndex(["2017-01-01"], freq="D"))
    True
    """

    if isinstance(arr, (ABCPeriodIndex, ABCPeriodArray)):
        return True
    elif isinstance(arr, (np.ndarray, ABCSeries)):
        return is_period_dtype(arr.dtype)
    return getattr(arr, "inferred_type", None) == "period"
