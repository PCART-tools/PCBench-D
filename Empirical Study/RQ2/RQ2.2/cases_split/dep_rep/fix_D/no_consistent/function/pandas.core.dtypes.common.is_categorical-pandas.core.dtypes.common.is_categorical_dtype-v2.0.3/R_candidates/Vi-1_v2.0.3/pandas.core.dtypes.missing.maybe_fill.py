def maybe_fill(arr: np.ndarray) -> np.ndarray:
    """
    Fill numpy.ndarray with NaN, unless we have a integer or boolean dtype.
    """
    if arr.dtype.kind not in ("u", "i", "b"):
        arr.fill(np.nan)
    return arr
