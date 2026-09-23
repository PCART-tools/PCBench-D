def is_datetime_or_timedelta_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of
    a timedelta64 or datetime64 dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a timedelta64,
        or datetime64 dtype.

    Examples
    --------
    >>> is_datetime_or_timedelta_dtype(str)
    False
    >>> is_datetime_or_timedelta_dtype(int)
    False
    >>> is_datetime_or_timedelta_dtype(np.datetime64)
    True
    >>> is_datetime_or_timedelta_dtype(np.timedelta64)
    True
    >>> is_datetime_or_timedelta_dtype(np.array(['a', 'b']))
    False
    >>> is_datetime_or_timedelta_dtype(pd.Series([1, 2]))
    False
    >>> is_datetime_or_timedelta_dtype(np.array([], dtype=np.timedelta64))
    True
    >>> is_datetime_or_timedelta_dtype(np.array([], dtype=np.datetime64))
    True
    """

    return _is_dtype_type(arr_or_dtype, classes(np.datetime64, np.timedelta64))
