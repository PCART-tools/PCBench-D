def polars_type_to_constructor(
    dtype: PolarsDataType,
) -> Callable[[str, Sequence[Any], bool], PySeries]:
    """Get the right PySeries constructor for the given Polars dtype."""
    try:
        base_type = dtype.base_type()
        # special case for Array as it needs to pass the width argument
        # upon construction
        if base_type == dt.Array:
            return functools.partial(PySeries.new_array, dtype.width, dtype.inner)  # type: ignore[union-attr]

        return _POLARS_TYPE_TO_CONSTRUCTOR[base_type]
    except KeyError:  # pragma: no cover
        raise ValueError(f"cannot construct PySeries for type {dtype!r}") from None
