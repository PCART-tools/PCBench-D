def is_signed_integer_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a signed integer dtype.

    Unlike in `in_any_int_dtype`, timedelta64 instances will return False.

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
        Whether or not the array or dtype is of a signed integer dtype
        and not an instance of timedelta64.

    Examples
    --------
    >>> is_signed_integer_dtype(str)
    False
    >>> is_signed_integer_dtype(int)
    True
    >>> is_signed_integer_dtype(float)
    False
    >>> is_signed_integer_dtype(np.uint64)  # unsigned
    False
    >>> is_signed_integer_dtype('int8')
    True
    >>> is_signed_integer_dtype('Int8')
    True
    >>> is_signed_integer_dtype(pd.Int8Dtype)
    True
    >>> is_signed_integer_dtype(np.datetime64)
    False
    >>> is_signed_integer_dtype(np.timedelta64)
    False
    >>> is_signed_integer_dtype(np.array(['a', 'b']))
    False
    >>> is_signed_integer_dtype(pd.Series([1, 2]))
    True
    >>> is_signed_integer_dtype(np.array([], dtype=np.timedelta64))
    False
    >>> is_signed_integer_dtype(pd.Index([1, 2.]))  # float
    False
    >>> is_signed_integer_dtype(np.array([1, 2], dtype=np.uint32))  # unsigned
    False
    """
    return _is_dtype_type(arr_or_dtype, classes_and_not_datetimelike(np.signedinteger))
