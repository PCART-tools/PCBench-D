def maybe_box_native(value: Scalar | None | NAType) -> Scalar | None | NAType:
    """
    If passed a scalar cast the scalar to a python native type.

    Parameters
    ----------
    value : scalar or Series

    Returns
    -------
    scalar or Series
    """
    if is_float(value):
        # error: Argument 1 to "float" has incompatible type
        # "Union[Union[str, int, float, bool], Union[Any, Timestamp, Timedelta, Any]]";
        # expected "Union[SupportsFloat, _SupportsIndex, str]"
        value = float(value)  # type: ignore[arg-type]
    elif is_integer(value):
        # error: Argument 1 to "int" has incompatible type
        # "Union[Union[str, int, float, bool], Union[Any, Timestamp, Timedelta, Any]]";
        # expected "Union[str, SupportsInt, _SupportsIndex, _SupportsTrunc]"
        value = int(value)  # type: ignore[arg-type]
    elif is_bool(value):
        value = bool(value)
    elif isinstance(value, (np.datetime64, np.timedelta64)):
        value = maybe_box_datetimelike(value)
    elif value is NA:
        value = None
    return value
