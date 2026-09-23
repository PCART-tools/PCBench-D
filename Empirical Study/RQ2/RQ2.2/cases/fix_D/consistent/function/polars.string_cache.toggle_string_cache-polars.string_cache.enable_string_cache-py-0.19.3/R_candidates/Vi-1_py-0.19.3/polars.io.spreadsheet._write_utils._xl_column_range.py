def _xl_column_range(
    df: DataFrame,
    table_start: tuple[int, int],
    col: str | tuple[int, int],
    *,
    has_header: bool,
    as_range: bool = True,
) -> tuple[int, int, int, int] | str:
    """Return the excel sheet range of a named column, accounting for all offsets."""
    col_start = (
        table_start[0] + int(has_header),
        table_start[1] + df.find_idx_by_name(col) if isinstance(col, str) else col[0],
    )
    col_finish = (
        col_start[0] + len(df) - 1,
        col_start[1] + 0 if isinstance(col, str) else (col[1] - col[0]),
    )
    if as_range:
        return "".join(_xl_rowcols_to_range(*col_start, *col_finish))
    else:
        return col_start + col_finish
