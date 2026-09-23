def _xl_column_multi_range(
    df: DataFrame,
    table_start: tuple[int, int],
    cols: Iterable[str],
    has_header: bool,
) -> str:
    """Return column ranges as an xlsxwriter 'multi_range' string, or spanning range."""
    m: dict[str, Any] = {}
    if _adjacent_cols(df, cols, min_max=m):
        return _xl_column_range(
            df, table_start, (m["min"]["idx"], m["max"]["idx"]), has_header
        )
    return " ".join(_xl_column_range(df, table_start, col, has_header) for col in cols)
