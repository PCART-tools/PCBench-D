def _scan_parquet_impl(  # noqa: D417
    uri: str, with_columns: list[str] | None, *args: Any, **kwargs: Any
) -> DataFrame:
    """
    Take the projected columns and materialize an arrow table.

    Parameters
    ----------
    uri
        Source URI
    with_columns
        Columns that are projected

    """
    import polars as pl

    return pl.read_parquet(uri, with_columns, *args, **kwargs)
