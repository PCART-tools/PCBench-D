def maybe_fill(arr, fill_value=np.nan):
    """
    if we have a compatible fill_value and arr dtype, then fill
    """
    if isna_compat(arr, fill_value):
        arr.fill(fill_value)
    return arr
