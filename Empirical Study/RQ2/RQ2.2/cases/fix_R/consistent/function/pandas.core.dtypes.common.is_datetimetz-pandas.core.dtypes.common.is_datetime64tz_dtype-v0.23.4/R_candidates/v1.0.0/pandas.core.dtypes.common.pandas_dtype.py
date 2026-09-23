def pandas_dtype(dtype):
    """
    Convert input into a pandas only dtype object or a numpy dtype object.

    Parameters
    ----------
    dtype : object to be converted

    Returns
    -------
    np.dtype or a pandas dtype

    Raises
    ------
    TypeError if not a dtype
    """
    # short-circuit
    if isinstance(dtype, np.ndarray):
        return dtype.dtype
    elif isinstance(dtype, (np.dtype, ExtensionDtype)):
        return dtype

    # registered extension types
    result = registry.find(dtype)
    if result is not None:
        return result

    # try a numpy dtype
    # raise a consistent TypeError if failed
    try:
        npdtype = np.dtype(dtype)
    except SyntaxError:
        # np.dtype uses `eval` which can raise SyntaxError
        raise TypeError(f"data type '{dtype}' not understood")

    # Any invalid dtype (such as pd.Timestamp) should raise an error.
    # np.dtype(invalid_type).kind = 0 for such objects. However, this will
    # also catch some valid dtypes such as object, np.object_ and 'object'
    # which we safeguard against by catching them earlier and returning
    # np.dtype(valid_dtype) before this condition is evaluated.
    if is_hashable(dtype) and dtype in [object, np.object_, "object", "O"]:
        # check hashability to avoid errors/DeprecationWarning when we get
        # here and `dtype` is an array
        return npdtype
    elif npdtype.kind == "O":
        raise TypeError(f"dtype '{dtype}' not understood")

    return npdtype
