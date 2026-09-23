def is_interval_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the Interval dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the Interval dtype.

    Examples
    --------
    >>> is_interval_dtype(object)
    False
    >>> is_interval_dtype(IntervalDtype())
    True
    >>> is_interval_dtype([1, 2, 3])
    False
    >>>
    >>> interval = pd.Interval(1, 2, closed="right")
    >>> is_interval_dtype(interval)
    False
    >>> is_interval_dtype(pd.IntervalIndex([interval]))
    True
    """

    # TODO: Consider making Interval an instance of IntervalDtype
    if arr_or_dtype is None:
        return False
    return IntervalDtype.is_dtype(arr_or_dtype)
