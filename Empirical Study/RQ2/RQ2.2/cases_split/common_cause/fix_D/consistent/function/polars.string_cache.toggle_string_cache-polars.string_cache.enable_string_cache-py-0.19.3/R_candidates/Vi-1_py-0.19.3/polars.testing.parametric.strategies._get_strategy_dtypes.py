def _get_strategy_dtypes(
    *,
    base_type: bool = False,
    excluding: tuple[PolarsDataType] | PolarsDataType | None = None,
) -> list[PolarsDataType]:
    """
    Get a list of all the dtypes for which we have a strategy.

    Parameters
    ----------
    base_type
        If True, return the base types for each dtype (eg:``List(Utf8)`` → ``List``).
    excluding
        A dtype or sequence of dtypes to omit from the results.

    """
    excluding = (excluding,) if is_polars_dtype(excluding) else (excluding or ())  # type: ignore[assignment]
    strategy_dtypes = list(chain(scalar_strategies.keys(), nested_strategies.keys()))
    return [
        (tp.base_type() if base_type else tp)
        for tp in strategy_dtypes
        if tp not in excluding  # type: ignore[operator]
    ]
