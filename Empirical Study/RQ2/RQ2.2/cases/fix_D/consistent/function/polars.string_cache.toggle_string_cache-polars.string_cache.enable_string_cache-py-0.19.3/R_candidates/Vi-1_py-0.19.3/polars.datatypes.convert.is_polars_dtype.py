def is_polars_dtype(dtype: Any, *, include_unknown: bool = False) -> bool:
    """Indicate whether the given input is a Polars dtype, or dtype specialisation."""
    try:
        if dtype == Unknown:
            # does not represent a realisable dtype, so ignore by default
            return include_unknown
        else:
            return isinstance(dtype, (DataType, DataTypeClass))
    except TypeError:
        return False
