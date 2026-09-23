def _xl_inject_sparklines(
    ws: Worksheet,
    df: DataFrame,
    table_start: tuple[int, int],
    col: str,
    *,
    has_header: bool,
    params: Sequence[str] | dict[str, Any],
) -> None:
    """Inject sparklines into (previously-created) empty table columns."""
    from xlsxwriter.utility import xl_rowcol_to_cell

    m: dict[str, Any] = {}
    data_cols = params.get("columns") if isinstance(params, dict) else params
    if not data_cols:
        raise ValueError("supplying 'columns' param value is mandatory for sparklines")
    elif not _adjacent_cols(df, data_cols, min_max=m):
        raise RuntimeError("sparkline data range/cols must all be adjacent")

    spk_row, spk_col, _, _ = _xl_column_range(
        df, table_start, col, has_header=has_header, as_range=False
    )
    data_start_col = table_start[1] + m["min"]["idx"]
    data_end_col = table_start[1] + m["max"]["idx"]

    if not isinstance(params, dict):
        options = {}
    else:
        # strip polars-specific params before passing to xlsxwriter
        options = {
            name: val
            for name, val in params.items()
            if name not in ("columns", "insert_after", "insert_before")
        }
        if "negative_points" not in options:
            options["negative_points"] = options.get("type") in ("column", "win_loss")

    for _ in range(len(df)):
        data_start = xl_rowcol_to_cell(spk_row, data_start_col)
        data_end = xl_rowcol_to_cell(spk_row, data_end_col)
        options["range"] = f"{data_start}:{data_end}"
        ws.add_sparkline(spk_row, spk_col, options)
        spk_row += 1
