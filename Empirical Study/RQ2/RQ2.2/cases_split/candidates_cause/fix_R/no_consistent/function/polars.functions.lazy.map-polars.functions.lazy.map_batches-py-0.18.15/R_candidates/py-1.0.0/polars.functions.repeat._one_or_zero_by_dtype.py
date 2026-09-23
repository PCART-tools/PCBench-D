@lru_cache(16)
def _one_or_zero_by_dtype(value: int, dtype: PolarsDataType) -> Any:
    if dtype in INTEGER_DTYPES:
        return value
    elif dtype in FLOAT_DTYPES:
        return float(value)
    elif dtype == Boolean:
        return bool(value)
    elif dtype == Utf8:
        return str(value)
    elif isinstance(dtype, Decimal):
        return D(value)
    elif isinstance(dtype, (List, Array)):
        arr_width = getattr(dtype, "size", 1)
        return [_one_or_zero_by_dtype(value, dtype.inner)] * arr_width
    return None
