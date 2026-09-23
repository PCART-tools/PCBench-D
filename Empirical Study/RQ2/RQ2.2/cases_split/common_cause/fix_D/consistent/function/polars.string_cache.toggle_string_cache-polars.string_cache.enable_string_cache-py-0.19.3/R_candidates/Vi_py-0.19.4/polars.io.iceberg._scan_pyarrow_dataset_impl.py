def _scan_pyarrow_dataset_impl(
    tbl: Table,
    with_columns: list[str] | None = None,
    predicate: str = "",
    n_rows: int | None = None,
    **kwargs: Any,
) -> DataFrame | Series:
    """
    Take the projected columns and materialize an arrow table.

    Parameters
    ----------
    tbl
        pyarrow dataset
    with_columns
        Columns that are projected
    predicate
        pyarrow expression that can be evaluated with eval
    n_rows:
        Materialize only n rows from the arrow dataset.
    batch_size
        The maximum row count for scanned pyarrow record batches.
    kwargs:
        For backward compatibility

    Returns
    -------
    DataFrame

    """
    from polars import from_arrow

    scan = tbl.scan(limit=n_rows)

    if with_columns is not None:
        scan = scan.select(*with_columns)

    if predicate is not None:
        try:
            expr_ast = _to_ast(predicate)
            pyiceberg_expr = _convert_predicate(expr_ast)
        except ValueError as e:
            raise ValueError(
                f"Could not convert predicate to PyIceberg: {predicate}"
            ) from e

        scan = scan.filter(pyiceberg_expr)

    return from_arrow(scan.to_arrow())
