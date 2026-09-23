def _maybe_fill(arr, fill_value=np.nan):
    """
    if we have a compatiable fill_value and arr dtype, then fill
    """
    if _is_na_compat(arr, fill_value):
        arr.fill(fill_value)
    return arr
