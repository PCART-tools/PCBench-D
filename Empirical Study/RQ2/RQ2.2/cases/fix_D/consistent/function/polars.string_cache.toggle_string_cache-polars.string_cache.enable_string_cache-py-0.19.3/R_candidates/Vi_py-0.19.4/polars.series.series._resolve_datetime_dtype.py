def _resolve_datetime_dtype(
    dtype: PolarsDataType | None, ndtype: np.datetime64
) -> PolarsDataType | None:
    """Given polars/numpy datetime dtypes, resolve to an explicit unit."""
    if dtype is None or (dtype == Datetime and not getattr(dtype, "time_unit", None)):
        time_unit = getattr(dtype, "time_unit", None) or np.datetime_data(ndtype)[0]
        # explicit formulation is verbose, but keeps mypy happy
        # (and avoids unsupported timeunits such as "s")
        if time_unit == "ns":
            dtype = Datetime("ns")
        elif time_unit == "us":
            dtype = Datetime("us")
        elif time_unit == "ms":
            dtype = Datetime("ms")
        elif time_unit == "D":
            dtype = Date
    return dtype
