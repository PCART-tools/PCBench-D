def _xl_apply_conditional_formats(
    df: DataFrame,
    ws: Worksheet,
    *,
    conditional_formats: ConditionalFormatDict,
    table_start: tuple[int, int],
    has_header: bool,
    format_cache: _XLFormatCache,
) -> None:
    """Take all conditional formatting options and apply them to the table/range."""
    from xlsxwriter.format import Format

    for cols, formats in _expand_selector_dicts(
        df, conditional_formats, expand_keys=True, expand_values=False, tuple_keys=True
    ).items():
        if not isinstance(cols, str) and len(cols) == 1:
            cols = next(iter(cols))
        if isinstance(formats, (str, dict)):
            formats = [formats]

        for fmt in formats:
            if not isinstance(fmt, dict):
                fmt = {"type": fmt}
            if isinstance(cols, str):
                col_range = _xl_column_range(
                    df, table_start, cols, has_header=has_header
                )
            else:
                col_range = _xl_column_multi_range(
                    df, table_start, cols, has_header=has_header
                )
                if " " in col_range:
                    col = next(iter(cols))
                    fmt["multi_range"] = col_range
                    col_range = _xl_column_range(
                        df, table_start, col, has_header=has_header
                    )

            if "format" in fmt:
                f = fmt["format"]
                fmt["format"] = (
                    f  # already registered
                    if isinstance(f, Format)
                    else format_cache.get(
                        {"num_format": f} if isinstance(f, str) else f
                    )
                )
            ws.conditional_format(col_range, fmt)
