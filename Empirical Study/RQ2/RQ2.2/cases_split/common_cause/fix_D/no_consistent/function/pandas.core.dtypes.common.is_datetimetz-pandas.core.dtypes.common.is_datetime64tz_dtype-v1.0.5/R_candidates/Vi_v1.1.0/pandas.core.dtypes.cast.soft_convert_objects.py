def soft_convert_objects(
    values: np.ndarray,
    datetime: bool = True,
    numeric: bool = True,
    timedelta: bool = True,
    coerce: bool = False,
    copy: bool = True,
):
    """ if we have an object dtype, try to coerce dates and/or numbers """
    validate_bool_kwarg(datetime, "datetime")
    validate_bool_kwarg(numeric, "numeric")
    validate_bool_kwarg(timedelta, "timedelta")
    validate_bool_kwarg(coerce, "coerce")
    validate_bool_kwarg(copy, "copy")

    conversion_count = sum((datetime, numeric, timedelta))
    if conversion_count == 0:
        raise ValueError("At least one of datetime, numeric or timedelta must be True.")
    elif conversion_count > 1 and coerce:
        raise ValueError(
            "Only one of 'datetime', 'numeric' or "
            "'timedelta' can be True when when coerce=True."
        )

    if not is_object_dtype(values.dtype):
        # If not object, do not attempt conversion
        values = values.copy() if copy else values
        return values

    # If 1 flag is coerce, ensure 2 others are False
    if coerce:
        # Immediate return if coerce
        if datetime:
            from pandas import to_datetime

            return to_datetime(values, errors="coerce").to_numpy()
        elif timedelta:
            from pandas import to_timedelta

            return to_timedelta(values, errors="coerce").to_numpy()
        elif numeric:
            from pandas import to_numeric

            return to_numeric(values, errors="coerce")

    # Soft conversions
    if datetime:
        # GH 20380, when datetime is beyond year 2262, hence outside
        # bound of nanosecond-resolution 64-bit integers.
        try:
            values = lib.maybe_convert_objects(values, convert_datetime=True)
        except OutOfBoundsDatetime:
            pass

    if timedelta and is_object_dtype(values.dtype):
        # Object check to ensure only run if previous did not convert
        values = lib.maybe_convert_objects(values, convert_timedelta=True)

    if numeric and is_object_dtype(values.dtype):
        try:
            converted = lib.maybe_convert_numeric(values, set(), coerce_numeric=True)
        except (ValueError, TypeError):
            pass
        else:
            # If all NaNs, then do not-alter
            values = converted if not isna(converted).all() else values
            values = values.copy() if copy else values

    return values
