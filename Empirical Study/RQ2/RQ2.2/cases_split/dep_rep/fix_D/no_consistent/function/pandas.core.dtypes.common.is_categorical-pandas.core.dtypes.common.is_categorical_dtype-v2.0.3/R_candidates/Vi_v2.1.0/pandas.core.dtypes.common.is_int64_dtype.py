def is_int64_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of the int64 dtype.

    .. deprecated:: 2.1.0

       is_int64_dtype is deprecated and will be removed in a future
       version. Use dtype == np.int64 instead.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of the int64 dtype.

    Notes
    -----
    Depending on system architecture, the return value of `is_int64_dtype(
    int)` will be True if the OS uses 64-bit integers and False if the OS
    uses 32-bit integers.

    Examples
    --------
    >>> from pandas.api.types import is_int64_dtype
    >>> is_int64_dtype(str)  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.int32)  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.int64)  # doctest: +SKIP
    True
    >>> is_int64_dtype('int8')  # doctest: +SKIP
    False
    >>> is_int64_dtype('Int8')  # doctest: +SKIP
    False
    >>> is_int64_dtype(pd.Int64Dtype)  # doctest: +SKIP
    True
    >>> is_int64_dtype(float)  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.uint64)  # unsigned  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.array(['a', 'b']))  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.array([1, 2], dtype=np.int64))  # doctest: +SKIP
    True
    >>> is_int64_dtype(pd.Index([1, 2.]))  # float  # doctest: +SKIP
    False
    >>> is_int64_dtype(np.array([1, 2], dtype=np.uint32))  # unsigned  # doctest: +SKIP
    False
    """
    # GH#52564
    warnings.warn(
        "is_int64_dtype is deprecated and will be removed in a future "
        "version. Use dtype == np.int64 instead.",
        FutureWarning,
        stacklevel=find_stack_level(),
    )
    return _is_dtype_type(arr_or_dtype, classes(np.int64))
