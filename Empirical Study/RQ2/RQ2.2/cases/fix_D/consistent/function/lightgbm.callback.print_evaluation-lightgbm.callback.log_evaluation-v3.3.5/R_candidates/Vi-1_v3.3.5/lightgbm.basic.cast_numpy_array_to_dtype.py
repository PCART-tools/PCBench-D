def cast_numpy_array_to_dtype(array, dtype):
    """Cast numpy array to given dtype."""
    if array.dtype == dtype:
        return array
    return array.astype(dtype=dtype, copy=False)
