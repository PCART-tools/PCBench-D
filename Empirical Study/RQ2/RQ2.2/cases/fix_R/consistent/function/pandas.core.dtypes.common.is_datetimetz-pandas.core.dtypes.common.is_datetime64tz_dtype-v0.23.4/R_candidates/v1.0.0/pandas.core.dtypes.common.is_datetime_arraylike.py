def is_datetime_arraylike(arr) -> bool:
    """
    Check whether an array-like is a datetime array-like or DatetimeIndex.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean
        Whether or not the array-like is a datetime array-like or
        DatetimeIndex.

    Examples
    --------
    >>> is_datetime_arraylike([1, 2, 3])
    False
    >>> is_datetime_arraylike(pd.Index([1, 2, 3]))
    False
    >>> is_datetime_arraylike(pd.DatetimeIndex([1, 2, 3]))
    True
    """

    if isinstance(arr, ABCDatetimeIndex):
        return True
    elif isinstance(arr, (np.ndarray, ABCSeries)):
        return (
            is_object_dtype(arr.dtype)
            and lib.infer_dtype(arr, skipna=False) == "datetime"
        )
    return getattr(arr, "inferred_type", None) == "datetime"
