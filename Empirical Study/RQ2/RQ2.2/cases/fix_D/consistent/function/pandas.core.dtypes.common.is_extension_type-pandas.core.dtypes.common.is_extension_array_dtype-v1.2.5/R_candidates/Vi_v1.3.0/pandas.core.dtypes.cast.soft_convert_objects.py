def soft_convert_objects(
    values: np.ndarray,
    datetime: bool = True,
    numeric: bool = True,
    timedelta: bool = True,
    period: bool = True,
    copy: bool = True,
) -> ArrayLike:
    """
    Try to coerce datetime, timedelta, and numeric object-dtype columns
    to inferred dtype.

    Parameters
    ----------
    values : np.ndarray[object]
    datetime : bool, default True
    numeric: bool, default True
    timedelta : bool, default True
    period : bool, default True
    copy : bool, default True

    Returns
    -------
    np.ndarray or ExtensionArray
    """
    validate_bool_kwarg(datetime, "datetime")
    validate_bool_kwarg(numeric, "numeric")
    validate_bool_kwarg(timedelta, "timedelta")
    validate_bool_kwarg(copy, "copy")

    conversion_count = sum((datetime, numeric, timedelta))
    if conversion_count == 0:
        raise ValueError("At least one of datetime, numeric or timedelta must be True.")

    # Soft conversions
    if datetime or timedelta:
        # GH 20380, when datetime is beyond year 2262, hence outside
        # bound of nanosecond-resolution 64-bit integers.
        try:
            converted = lib.maybe_convert_objects(
                values,
                convert_datetime=datetime,
                convert_timedelta=timedelta,
                convert_period=period,
            )
        except (OutOfBoundsDatetime, ValueError):
            return values
        if converted is not values:
            return converted

    if numeric and is_object_dtype(values.dtype):
        converted, _ = lib.maybe_convert_numeric(values, set(), coerce_numeric=True)

        # If all NaNs, then do not-alter
        values = converted if not isna(converted).all() else values
        values = values.copy() if copy else values

    return values
