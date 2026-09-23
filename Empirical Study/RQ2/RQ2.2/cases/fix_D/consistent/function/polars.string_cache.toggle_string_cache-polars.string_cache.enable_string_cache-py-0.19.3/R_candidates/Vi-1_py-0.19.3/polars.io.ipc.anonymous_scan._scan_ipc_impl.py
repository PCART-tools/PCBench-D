def _scan_ipc_impl(  # noqa: D417
    source: str,
    columns: list[str] | None,
    predicate: str | None,
    n_rows: int | None,
    **kwargs: Any,
) -> DataFrame:
    """
    Take the projected columns and materialize an arrow table.

    Parameters
    ----------
    source
        Source URI
    columns
        Columns that are projected

    """
    from polars import read_ipc

    return read_ipc(source, columns=columns, n_rows=n_rows, **kwargs)
