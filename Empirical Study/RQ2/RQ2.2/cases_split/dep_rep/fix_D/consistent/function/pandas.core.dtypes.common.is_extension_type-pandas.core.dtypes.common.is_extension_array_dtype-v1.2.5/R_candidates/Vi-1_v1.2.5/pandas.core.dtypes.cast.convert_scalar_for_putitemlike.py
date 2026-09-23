def convert_scalar_for_putitemlike(scalar: Scalar, dtype: np.dtype) -> Scalar:
    """
    Convert datetimelike scalar if we are setting into a datetime64
    or timedelta64 ndarray.

    Parameters
    ----------
    scalar : scalar
    dtype : np.dtype

    Returns
    -------
    scalar
    """
    if dtype.kind == "m":
        if isinstance(scalar, (timedelta, np.timedelta64)):
            # We have to cast after asm8 in case we have NaT
            return Timedelta(scalar).asm8.view("timedelta64[ns]")
        elif scalar is None or scalar is NaT or (is_float(scalar) and np.isnan(scalar)):
            return np.timedelta64("NaT", "ns")
    if dtype.kind == "M":
        if isinstance(scalar, (date, np.datetime64)):
            # Note: we include date, not just datetime
            return Timestamp(scalar).to_datetime64()
        elif scalar is None or scalar is NaT or (is_float(scalar) and np.isnan(scalar)):
            return np.datetime64("NaT", "ns")
    else:
        validate_numeric_casting(dtype, scalar)
    return scalar
