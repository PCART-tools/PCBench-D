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
    if dtype.kind in ["m", "M"]:
        scalar = maybe_box_datetimelike(scalar, dtype)
        return maybe_unbox_datetimelike(scalar, dtype)
    else:
        validate_numeric_casting(dtype, scalar)
    return scalar
