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
    # error: Argument 1 to "__call__" of "ufunc" has incompatible type
    # "Union[Union[str, int, float, bool], Union[Any, Timestamp, Timedelta, Any]]";
    # expected "Union[Union[int, float, complex, str, bytes, generic],
    # Sequence[Union[int, float, complex, str, bytes, generic]],
    # Sequence[Sequence[Any]], _SupportsArray]"
    if (
        issubclass(dtype.type, (np.integer, np.bool_))
        and is_float(value)
        and np.isnan(value)  # type: ignore[arg-type]
    ):
        raise ValueError("Cannot assign nan to integer series")

    elif dtype.kind in ["i", "u", "f", "c"]:
        if is_bool(value) or isinstance(value, np.timedelta64):
            # numpy will cast td64 to integer if we're not careful
            raise ValueError(
                f"Cannot assign {type(value).__name__} to float/integer series"
            )
    elif dtype.kind == "b":
        if is_scalar(value) and not is_bool(value):
            raise ValueError(f"Cannot assign {type(value).__name__} to bool series")
