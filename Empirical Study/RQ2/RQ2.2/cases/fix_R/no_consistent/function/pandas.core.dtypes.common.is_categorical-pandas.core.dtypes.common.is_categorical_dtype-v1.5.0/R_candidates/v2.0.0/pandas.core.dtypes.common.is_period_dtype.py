def is_period_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the Period dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the Period dtype.

    Examples
    --------
    >>> is_period_dtype(object)
    False
    >>> is_period_dtype(PeriodDtype(freq="D"))
    True
    >>> is_period_dtype([1, 2, 3])
    False
    >>> is_period_dtype(pd.Period("2017-01-01"))
    False
    >>> is_period_dtype(pd.PeriodIndex([], freq="A"))
    True
    """
    if isinstance(arr_or_dtype, ExtensionDtype):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.type is Period

    if arr_or_dtype is None:
        return False
    return PeriodDtype.is_dtype(arr_or_dtype)
