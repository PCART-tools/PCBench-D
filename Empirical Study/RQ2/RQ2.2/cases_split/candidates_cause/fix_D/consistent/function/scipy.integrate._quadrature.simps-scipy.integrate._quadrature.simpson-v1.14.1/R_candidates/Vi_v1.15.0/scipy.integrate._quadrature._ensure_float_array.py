def _ensure_float_array(arr: npt.ArrayLike) -> np.ndarray:
    arr = np.asarray(arr)
    if np.issubdtype(arr.dtype, np.integer):
        arr = arr.astype(float, copy=False)
    return arr
