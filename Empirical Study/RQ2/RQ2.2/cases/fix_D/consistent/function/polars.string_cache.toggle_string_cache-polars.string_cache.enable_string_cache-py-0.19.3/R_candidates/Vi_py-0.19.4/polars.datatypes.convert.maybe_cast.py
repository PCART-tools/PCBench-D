def maybe_cast(el: Any, dtype: PolarsDataType) -> Any:
    """Try casting a value to a value that is valid for the given Polars dtype."""
    # cast el if it doesn't match
    from polars.utils.convert import (
        _datetime_to_pl_timestamp,
        _timedelta_to_pl_timedelta,
    )

    try:
        time_unit = dtype.time_unit  # type: ignore[union-attr]
    except AttributeError:
        time_unit = None

    if isinstance(el, datetime):
        return _datetime_to_pl_timestamp(el, time_unit)
    elif isinstance(el, timedelta):
        return _timedelta_to_pl_timedelta(el, time_unit)

    py_type = dtype_to_py_type(dtype)
    if not isinstance(el, py_type):
        try:
            el = py_type(el)  # type: ignore[call-arg, misc]
        except Exception:
            raise TypeError(
                f"cannot convert Python type {type(el).__name__!r} to {dtype!r}"
            ) from None
    return el
