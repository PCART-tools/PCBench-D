def is_string_like_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a string-like dtype.

    Unlike `is_string_dtype`, the object dtype is excluded because it
    is a mixed dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of the string dtype.

    Examples
    --------
    >>> is_string_like_dtype(str)
    True
    >>> is_string_like_dtype(object)
    False
    >>> is_string_like_dtype(np.array(['a', 'b']))
    True
    >>> is_string_like_dtype(pd.Series([1, 2]))
    False
    """

    return _is_dtype(arr_or_dtype, lambda dtype: dtype.kind in ("S", "U"))
