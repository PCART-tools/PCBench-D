def maybe_castable(arr: np.ndarray) -> bool:
    # return False to force a non-fastpath

    assert isinstance(arr, np.ndarray)  # GH 37024

    # check datetime64[ns]/timedelta64[ns] are valid
    # otherwise try to coerce
    kind = arr.dtype.kind
    if kind == "M":
        return is_datetime64_ns_dtype(arr.dtype)
    elif kind == "m":
        return is_timedelta64_ns_dtype(arr.dtype)

    return arr.dtype.name not in POSSIBLY_CAST_DTYPES
