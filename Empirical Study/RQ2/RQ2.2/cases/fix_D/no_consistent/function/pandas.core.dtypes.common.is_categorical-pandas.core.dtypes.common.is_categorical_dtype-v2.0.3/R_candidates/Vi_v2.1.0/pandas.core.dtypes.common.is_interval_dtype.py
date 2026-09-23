def is_interval_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the Interval dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the Interval dtype.

    Examples
    --------
    >>> from pandas.core.dtypes.common import is_interval_dtype
    >>> is_interval_dtype(object)
    False
    >>> is_interval_dtype(pd.IntervalDtype())
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
    # GH#52607
    warnings.warn(
        "is_interval_dtype is deprecated and will be removed in a future version. "
        "Use `isinstance(dtype, pd.IntervalDtype)` instead",
        FutureWarning,
        stacklevel=find_stack_level(),
    )
    if isinstance(arr_or_dtype, ExtensionDtype):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.type is Interval

    if arr_or_dtype is None:
        return False
    return IntervalDtype.is_dtype(arr_or_dtype)
