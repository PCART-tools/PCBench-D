def _possibly_castable(arr):
    # return False to force a non-fastpath

    # check datetime64[ns]/timedelta64[ns] are valid
    # otherwise try to coerce
    kind = arr.dtype.kind
    if kind == 'M' or kind == 'm':
        return arr.dtype in _DATELIKE_DTYPES

    return arr.dtype.name not in _POSSIBLY_CAST_DTYPES
