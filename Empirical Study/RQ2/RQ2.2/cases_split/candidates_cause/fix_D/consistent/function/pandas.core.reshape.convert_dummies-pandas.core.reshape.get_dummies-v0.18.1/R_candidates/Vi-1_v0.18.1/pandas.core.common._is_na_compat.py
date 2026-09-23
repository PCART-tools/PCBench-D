def _is_na_compat(arr, fill_value=np.nan):
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
    if isnull(fill_value):
        return not (is_bool_dtype(dtype) or
                    is_integer_dtype(dtype))
    return True
