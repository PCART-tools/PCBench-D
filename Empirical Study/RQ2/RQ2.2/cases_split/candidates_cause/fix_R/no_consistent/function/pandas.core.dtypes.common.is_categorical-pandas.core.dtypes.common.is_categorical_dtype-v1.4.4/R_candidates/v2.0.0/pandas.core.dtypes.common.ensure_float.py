def ensure_float(arr):
    """
    Ensure that an array object has a float dtype if possible.

    Parameters
    ----------
    arr : array-like
        The array whose data type we want to enforce as float.

    Returns
    -------
    float_arr : The original array cast to the float dtype if
                possible. Otherwise, the original array is returned.
    """
    if is_extension_array_dtype(arr.dtype):
        if is_float_dtype(arr.dtype):
            arr = arr.to_numpy(dtype=arr.dtype.numpy_dtype, na_value=np.nan)
        else:
            arr = arr.to_numpy(dtype="float64", na_value=np.nan)
    elif issubclass(arr.dtype.type, (np.integer, np.bool_)):
        arr = arr.astype(float)
    return arr
