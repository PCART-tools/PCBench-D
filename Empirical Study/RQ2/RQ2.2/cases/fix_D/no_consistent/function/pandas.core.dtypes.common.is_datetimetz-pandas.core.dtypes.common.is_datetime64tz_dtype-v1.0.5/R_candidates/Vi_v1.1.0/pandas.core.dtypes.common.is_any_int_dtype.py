def is_any_int_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of an integer dtype.

    In this function, timedelta64 instances are also considered "any-integer"
    type objects and will return True.

    This function is internal and should not be exposed in the public API.

    .. versionchanged:: 0.24.0

       The nullable Integer dtypes (e.g. pandas.Int64Dtype) are also considered
       as integer by this function.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of an integer dtype.

    Examples
    --------
    >>> is_any_int_dtype(str)
    False
    >>> is_any_int_dtype(int)
    True
    >>> is_any_int_dtype(float)
    False
    >>> is_any_int_dtype(np.uint64)
    True
    >>> is_any_int_dtype(np.datetime64)
    False
    >>> is_any_int_dtype(np.timedelta64)
    True
    >>> is_any_int_dtype(np.array(['a', 'b']))
    False
    >>> is_any_int_dtype(pd.Series([1, 2]))
    True
    >>> is_any_int_dtype(np.array([], dtype=np.timedelta64))
    True
    >>> is_any_int_dtype(pd.Index([1, 2.]))  # float
    False
    """
    return _is_dtype_type(arr_or_dtype, classes(np.integer, np.timedelta64))
