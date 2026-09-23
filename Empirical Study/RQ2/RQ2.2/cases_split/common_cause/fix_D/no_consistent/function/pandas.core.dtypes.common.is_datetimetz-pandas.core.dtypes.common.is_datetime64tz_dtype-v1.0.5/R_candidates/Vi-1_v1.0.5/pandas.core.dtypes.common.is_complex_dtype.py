def is_complex_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a complex dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a complex dtype.

    Examples
    --------
    >>> is_complex_dtype(str)
    False
    >>> is_complex_dtype(int)
    False
    >>> is_complex_dtype(np.complex)
    True
    >>> is_complex_dtype(np.array(['a', 'b']))
    False
    >>> is_complex_dtype(pd.Series([1, 2]))
    False
    >>> is_complex_dtype(np.array([1 + 1j, 5]))
    True
    """

    return _is_dtype_type(arr_or_dtype, classes(np.complexfloating))
