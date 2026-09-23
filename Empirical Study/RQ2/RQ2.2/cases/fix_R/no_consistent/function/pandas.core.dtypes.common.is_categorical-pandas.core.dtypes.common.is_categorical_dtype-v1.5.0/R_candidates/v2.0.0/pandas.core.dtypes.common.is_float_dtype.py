def is_float_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a float dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a float dtype.

    Examples
    --------
    >>> from pandas.api.types import is_float_dtype
    >>> is_float_dtype(str)
    False
    >>> is_float_dtype(int)
    False
    >>> is_float_dtype(float)
    True
    >>> is_float_dtype(np.array(['a', 'b']))
    False
    >>> is_float_dtype(pd.Series([1, 2]))
    False
    >>> is_float_dtype(pd.Index([1, 2.]))
    True
    """
    return _is_dtype_type(arr_or_dtype, classes(np.floating)) or _is_dtype(
        arr_or_dtype, lambda typ: isinstance(typ, ExtensionDtype) and typ.kind in "f"
    )
