def infer_dtype_from_array(arr, pandas_dtype: bool = False) -> Tuple[DtypeObj, Any]:
    """
    Infer the dtype from an array.

    Parameters
    ----------
    arr : array
    pandas_dtype : bool, default False
        whether to infer dtype including pandas extension types.
        If False, array belongs to pandas extension types
        is inferred as object

    Returns
    -------
    tuple (numpy-compat/pandas-compat dtype, array)

    Notes
    -----
    if pandas_dtype=False. these infer to numpy dtypes
    exactly with the exception that mixed / object dtypes
    are not coerced by stringifying or conversion

    if pandas_dtype=True. datetime64tz-aware/categorical
    types will retain there character.

    Examples
    --------
    >>> np.asarray([1, '1'])
    array(['1', '1'], dtype='<U21')

    >>> infer_dtype_from_array([1, '1'])
    (dtype('O'), [1, '1'])
    """
    if isinstance(arr, np.ndarray):
        return arr.dtype, arr

    if not is_list_like(arr):
        arr = [arr]

    if pandas_dtype and is_extension_array_dtype(arr):
        return arr.dtype, arr

    elif isinstance(arr, ABCSeries):
        return arr.dtype, np.asarray(arr)

    # don't force numpy coerce with nan's
    inferred = lib.infer_dtype(arr, skipna=False)
    if inferred in ["string", "bytes", "mixed", "mixed-integer"]:
        return (np.dtype(np.object_), arr)

    arr = np.asarray(arr)
    return arr.dtype, arr
