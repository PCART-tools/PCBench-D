def _cast_numpy_array_to_dtype(array: np.ndarray, dtype: "np.typing.DTypeLike") -> np.ndarray:
    """Cast numpy array to given dtype."""
    if array.dtype == dtype:
        return array
    return array.astype(dtype=dtype, copy=False)
