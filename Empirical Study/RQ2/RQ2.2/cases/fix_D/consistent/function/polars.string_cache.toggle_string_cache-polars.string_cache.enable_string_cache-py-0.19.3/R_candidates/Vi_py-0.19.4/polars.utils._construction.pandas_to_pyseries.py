def pandas_to_pyseries(
    name: str, values: pd.Series[Any] | pd.DatetimeIndex, *, nan_to_null: bool = True
) -> PySeries:
    """Construct a PySeries from a pandas Series or DatetimeIndex."""
    # TODO: Change `if not name` to `if name is not None` once name is Optional[str]
    if not name and values.name is not None:
        name = str(values.name)
    return arrow_to_pyseries(
        name, _pandas_series_to_arrow(values, nan_to_null=nan_to_null)
    )
