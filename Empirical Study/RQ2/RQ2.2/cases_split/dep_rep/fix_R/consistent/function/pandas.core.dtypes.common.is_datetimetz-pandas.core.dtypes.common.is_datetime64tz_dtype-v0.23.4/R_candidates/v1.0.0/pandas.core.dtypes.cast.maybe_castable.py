def maybe_castable(arr) -> bool:
    # return False to force a non-fastpath

    # check datetime64[ns]/timedelta64[ns] are valid
    # otherwise try to coerce
    kind = arr.dtype.kind
    if kind == "M":
        return is_datetime64_ns_dtype(arr.dtype)
    elif kind == "m":
        return is_timedelta64_ns_dtype(arr.dtype)

    return arr.dtype.name not in _POSSIBLY_CAST_DTYPES
