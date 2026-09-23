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
    if issubclass(arr.dtype.type, (np.integer, np.bool_)):
        arr = arr.astype(float)
    return arr
