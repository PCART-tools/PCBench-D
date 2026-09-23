def is_datetime64_any_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of the datetime64 dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of the datetime64 dtype.

    Examples
    --------
    >>> is_datetime64_any_dtype(str)
    False
    >>> is_datetime64_any_dtype(int)
    False
    >>> is_datetime64_any_dtype(np.datetime64)  # can be tz-naive
    True
    >>> is_datetime64_any_dtype(DatetimeTZDtype("ns", "US/Eastern"))
    True
    >>> is_datetime64_any_dtype(np.array(['a', 'b']))
    False
    >>> is_datetime64_any_dtype(np.array([1, 2]))
    False
    >>> is_datetime64_any_dtype(np.array([], dtype=np.datetime64))
    True
    >>> is_datetime64_any_dtype(pd.DatetimeIndex([1, 2, 3],
                                dtype=np.datetime64))
    True
    """

    if arr_or_dtype is None:
        return False
    return is_datetime64_dtype(arr_or_dtype) or is_datetime64tz_dtype(arr_or_dtype)
