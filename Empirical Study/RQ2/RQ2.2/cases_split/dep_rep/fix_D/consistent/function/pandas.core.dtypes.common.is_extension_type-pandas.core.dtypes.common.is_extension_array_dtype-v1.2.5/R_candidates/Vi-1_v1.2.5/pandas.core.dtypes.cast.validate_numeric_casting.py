def validate_numeric_casting(dtype: np.dtype, value: Scalar) -> None:
    """
    Check that we can losslessly insert the given value into an array
    with the given dtype.

    Parameters
    ----------
    dtype : np.dtype
    value : scalar

    Raises
    ------
    ValueError
    """
    if issubclass(dtype.type, (np.integer, np.bool_)):
        if is_float(value) and np.isnan(value):
            raise ValueError("Cannot assign nan to integer series")

    if issubclass(dtype.type, (np.integer, np.floating, complex)) and not issubclass(
        dtype.type, np.bool_
    ):
        if is_bool(value):
            raise ValueError("Cannot assign bool to float/integer series")
