def maybe_convert_objects(values: np.ndarray, convert_numeric: bool = True):
    """
    If we have an object dtype array, try to coerce dates and/or numbers.

    Parameters
    ----------
    values : ndarray
    convert_numeric : bool, default True

    Returns
    -------
    ndarray or DatetimeIndex
    """
    validate_bool_kwarg(convert_numeric, "convert_numeric")

    orig_values = values

    # convert dates
    if is_object_dtype(values.dtype):
        values = lib.maybe_convert_objects(values, convert_datetime=True)

    # convert timedeltas
    if is_object_dtype(values.dtype):
        values = lib.maybe_convert_objects(values, convert_timedelta=True)

    # convert to numeric
    if is_object_dtype(values.dtype):
        if convert_numeric:
            try:
                new_values = lib.maybe_convert_numeric(
                    values, set(), coerce_numeric=True
                )
            except (ValueError, TypeError):
                pass
            else:
                # if we are all nans then leave me alone
                if not isna(new_values).all():
                    values = new_values

        else:
            # soft-conversion
            values = lib.maybe_convert_objects(values)

    if values is orig_values:
        values = values.copy()

    return values
