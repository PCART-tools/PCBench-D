def _isna_compat(arr, fill_value=np.nan) -> bool:
    """
    Parameters
    ----------
    arr: a numpy array
    fill_value: fill value, default to np.nan

    Returns
    -------
    True if we can fill using this fill_value
    """
    dtype = arr.dtype
    if isna(fill_value):
        return not (is_bool_dtype(dtype) or is_integer_dtype(dtype))
    return True
