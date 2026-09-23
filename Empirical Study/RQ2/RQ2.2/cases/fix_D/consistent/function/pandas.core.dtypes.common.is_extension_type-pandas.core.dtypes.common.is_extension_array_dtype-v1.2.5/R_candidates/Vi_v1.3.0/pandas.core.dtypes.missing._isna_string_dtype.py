def _isna_string_dtype(values: np.ndarray, inf_as_na: bool) -> np.ndarray:
    # Working around NumPy ticket 1542
    dtype = values.dtype
    shape = values.shape

    if dtype.kind in ("S", "U"):
        result = np.zeros(values.shape, dtype=bool)
    else:
        result = np.empty(shape, dtype=bool)
        if inf_as_na:
            vec = libmissing.isnaobj_old(values.ravel())
        else:
            vec = libmissing.isnaobj(values.ravel())

        result[...] = vec.reshape(shape)

    return result
