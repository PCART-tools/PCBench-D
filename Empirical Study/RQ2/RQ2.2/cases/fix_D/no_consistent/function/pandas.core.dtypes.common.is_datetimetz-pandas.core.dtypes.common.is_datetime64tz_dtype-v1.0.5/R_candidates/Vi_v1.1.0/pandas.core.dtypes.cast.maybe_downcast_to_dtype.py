def maybe_downcast_to_dtype(result, dtype):
    """
    try to cast to the specified dtype (e.g. convert back to bool/int
    or could be an astype of float64->float32
    """
    do_round = False

    if is_scalar(result):
        return result
    elif isinstance(result, ABCDataFrame):
        # occurs in pivot_table doctest
        return result

    if isinstance(dtype, str):
        if dtype == "infer":
            inferred_type = lib.infer_dtype(ensure_object(result), skipna=False)
            if inferred_type == "boolean":
                dtype = "bool"
            elif inferred_type == "integer":
                dtype = "int64"
            elif inferred_type == "datetime64":
                dtype = "datetime64[ns]"
            elif inferred_type == "timedelta64":
                dtype = "timedelta64[ns]"

            # try to upcast here
            elif inferred_type == "floating":
                dtype = "int64"
                if issubclass(result.dtype.type, np.number):
                    do_round = True

            else:
                dtype = "object"

        dtype = np.dtype(dtype)

    converted = maybe_downcast_numeric(result, dtype, do_round)
    if converted is not result:
        return converted

    # a datetimelike
    # GH12821, iNaT is casted to float
    if dtype.kind in ["M", "m"] and result.dtype.kind in ["i", "f"]:
        if hasattr(dtype, "tz"):
            # not a numpy dtype
            if dtype.tz:
                # convert to datetime and change timezone
                from pandas import to_datetime

                result = to_datetime(result).tz_localize("utc")
                result = result.tz_convert(dtype.tz)
        else:
            result = result.astype(dtype)

    elif dtype.type is Period:
        # TODO(DatetimeArray): merge with previous elif
        from pandas.core.arrays import PeriodArray

        try:
            return PeriodArray(result, freq=dtype.freq)
        except TypeError:
            # e.g. TypeError: int() argument must be a string, a
            #  bytes-like object or a number, not 'Period
            pass

    return result
