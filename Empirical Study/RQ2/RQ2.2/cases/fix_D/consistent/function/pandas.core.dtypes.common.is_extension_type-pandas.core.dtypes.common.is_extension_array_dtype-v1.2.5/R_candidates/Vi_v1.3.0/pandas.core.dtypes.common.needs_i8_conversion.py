def needs_i8_conversion(arr_or_dtype) -> bool:
    """
    Check whether the array or dtype should be converted to int64.

    An array-like or dtype "needs" such a conversion if the array-like
    or dtype is of a datetime-like dtype

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype should be converted to int64.

    Examples
    --------
    >>> needs_i8_conversion(str)
    False
    >>> needs_i8_conversion(np.int64)
    False
    >>> needs_i8_conversion(np.datetime64)
    True
    >>> needs_i8_conversion(np.array(['a', 'b']))
    False
    >>> needs_i8_conversion(pd.Series([1, 2]))
    False
    >>> needs_i8_conversion(pd.Series([], dtype="timedelta64[ns]"))
    True
    >>> needs_i8_conversion(pd.DatetimeIndex([1, 2, 3], tz="US/Eastern"))
    True
    """
    if arr_or_dtype is None:
        return False
    if isinstance(arr_or_dtype, (np.dtype, ExtensionDtype)):
        # fastpath
        dtype = arr_or_dtype
        return dtype.kind in ["m", "M"] or dtype.type is Period
    return (
        is_datetime_or_timedelta_dtype(arr_or_dtype)
        or is_datetime64tz_dtype(arr_or_dtype)
        or is_period_dtype(arr_or_dtype)
    )
