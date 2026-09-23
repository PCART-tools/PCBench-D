def needs_i8_conversion(arr_or_dtype) -> bool:
    """
    Check whether the array or dtype should be converted to int64.

    An array-like or dtype "needs" such a conversion if the array-like
    or dtype is of a datetime-like dtype

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
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
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype.kind in ["m", "M"]
    elif isinstance(arr_or_dtype, ExtensionDtype):
        return isinstance(arr_or_dtype, (PeriodDtype, DatetimeTZDtype))

    try:
        dtype = get_dtype(arr_or_dtype)
    except (TypeError, ValueError):
        return False
    if isinstance(dtype, np.dtype):
        return dtype.kind in ["m", "M"]
    return isinstance(dtype, (PeriodDtype, DatetimeTZDtype))
