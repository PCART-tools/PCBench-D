def _scan_pyarrow_dataset_impl(
    ds: pa.dataset.Dataset,
    with_columns: list[str] | None,
    predicate: str | None,
    n_rows: int | None,
    batch_size: int | None,
) -> DataFrame:
    """
    Take the projected columns and materialize an arrow table.

    Parameters
    ----------
    ds
        pyarrow dataset
    with_columns
        Columns that are projected
    predicate
        pyarrow expression that can be evaluated with eval
    n_rows:
        Materialize only n rows from the arrow dataset
    batch_size
        The maximum row count for scanned pyarrow record batches.

    Returns
    -------
    DataFrame

    """
    from polars import from_arrow

    _filter = None
    if predicate:
        # imports are used by inline python evaluated by `eval`
        from polars.datatypes import Date, Datetime, Duration  # noqa: F401
        from polars.utils.convert import (
            _to_python_datetime,  # noqa: F401
            _to_python_time,  # noqa: F401
            _to_python_timedelta,  # noqa: F401
        )

        _filter = eval(predicate)

    common_params = {"columns": with_columns, "filter": _filter}
    if batch_size is not None:
        common_params["batch_size"] = batch_size

    if n_rows:
        return from_arrow(ds.head(n_rows, **common_params))  # type: ignore[return-value]

    return from_arrow(ds.to_table(**common_params))  # type: ignore[return-value]
