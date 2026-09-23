def _ensure_dtype_type(value, dtype):
    """
    Ensure that the given value is an instance of the given dtype.

    e.g. if out dtype is np.complex64_, we should have an instance of that
    as opposed to a python complex object.

    Parameters
    ----------
    value : object
    dtype : np.dtype or ExtensionDtype

    Returns
    -------
    object
    """
    # Start with exceptions in which we do _not_ cast to numpy types
    if is_extension_array_dtype(dtype):
        return value
    elif dtype == np.object_:
        return value
    elif isna(value):
        # e.g. keep np.nan rather than try to cast to np.float32(np.nan)
        return value

    return dtype.type(value)
