def nlargest(arr, n, keep='first'):
    """
    Find the indices of the n largest values of a numpy array.

    Note: Fails silently with NaN.
    """
    sdtype = str(arr.dtype)
    arr = arr.view(_dtype_map.get(sdtype, sdtype))
    return nsmallest(-arr, n, keep=keep)
