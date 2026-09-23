def _xl_setup_table_columns(
    df: DataFrame,
    wb: Workbook,
    format_cache: _XLFormatCache,
    column_totals: ColumnTotalsDefinition | None = None,
    column_formats: dict[str | tuple[str, ...], str] | None = None,
    dtype_formats: dict[OneOrMoreDataTypes, str] | None = None,
    sparklines: dict[str, Sequence[str] | dict[str, Any]] | None = None,
    row_totals: RowTotalsDefinition | None = None,
    float_precision: int = 3,
) -> tuple[list[dict[str, Any]], dict[str | tuple[str, ...], str], DataFrame]:
    """Setup and unify all column-related formatting/defaults."""
    column_totals = _unpack_multi_column_dict(column_totals)  # type: ignore[assignment]
    column_formats = _unpack_multi_column_dict(column_formats)  # type: ignore[assignment]

    # normalise column totals
    column_total_funcs = (
        {col: "sum" for col in column_totals}
        if isinstance(column_totals, Sequence)
        else (column_totals.copy() if isinstance(column_totals, dict) else {})
    )

    # normalise row totals
    if not row_totals:
        row_total_funcs = {}
    else:
        numeric_cols = {
            col for col, tp in df.schema.items() if tp.base_type() in NUMERIC_DTYPES
        }
        if not isinstance(row_totals, dict):
            sum_cols = (
                numeric_cols
                if row_totals is True
                else ({row_totals} if isinstance(row_totals, str) else set(row_totals))
            )
            n_ucase = sum((c[0] if c else "").isupper() for c in df.columns)
            total = f"{'T' if (n_ucase > len(df.columns) // 2) else 't'}otal"
            row_total_funcs = {total: _xl_table_formula(df, sum_cols, "sum")}
        else:
            row_total_funcs = {
                name: _xl_table_formula(
                    df, numeric_cols if cols is True else cols, "sum"
                )
                for name, cols in row_totals.items()
            }

    # normalise formats
    column_formats = (column_formats or {}).copy()
    dtype_formats = (dtype_formats or {}).copy()
    for tp in list(dtype_formats):
        if isinstance(tp, (tuple, frozenset)):
            dtype_formats.update(dict.fromkeys(tp, dtype_formats.pop(tp)))

    # inject sparkline/row-total placeholder(s)
    if sparklines:
        df = _xl_inject_dummy_table_columns(df, sparklines, value=None)
    if row_totals:
        df = _xl_inject_dummy_table_columns(df, row_total_funcs, value=0.0)

    # seed format cache with default fallback format
    fmt_default = format_cache.get({"valign": "vcenter"})

    # default float format
    zeros = "0" * float_precision
    fmt_float = (
        _XL_DEFAULT_INTEGER_FORMAT_
        if not zeros
        else _XL_DEFAULT_FLOAT_FORMAT_.replace(".000", f".{zeros}")
    )

    # assign default dtype formats
    for tp, fmt in _XL_DEFAULT_DTYPE_FORMATS_.items():
        dtype_formats.setdefault(tp, fmt)
    for tp in FLOAT_DTYPES:
        dtype_formats.setdefault(tp, fmt_float)
    for tp, fmt in dtype_formats.items():
        dtype_formats[tp] = fmt

    # associate formats/functions with specific columns
    for col, tp in df.schema.items():
        base_type = tp.base_type()
        if base_type in dtype_formats:
            fmt = dtype_formats.get(tp, dtype_formats[base_type])
            column_formats.setdefault(col, fmt)
        if base_type in NUMERIC_DTYPES:
            if column_totals is True:
                column_total_funcs.setdefault(col, "sum")
        if col not in column_formats:
            column_formats[col] = fmt_default

    # ensure externally supplied formats are made available
    for col, fmt in column_formats.items():  # type: ignore[assignment]
        if isinstance(fmt, str):
            column_formats[col] = format_cache.get(
                {"num_format": fmt, "valign": "vcenter"}
            )
        elif isinstance(fmt, dict):
            if "num_format" not in fmt:
                tp = df.schema.get(col)
                if tp in dtype_formats:
                    fmt["num_format"] = dtype_formats[tp]
            if "valign" not in fmt:
                fmt["valign"] = "vcenter"
            column_formats[col] = format_cache.get(fmt)

    # assemble table columns
    table_columns = [
        {
            k: v
            for k, v in {
                "header": col,
                "format": column_formats[col],
                "total_function": column_total_funcs.get(col),
                "formula": row_total_funcs.get(col),
            }.items()
            if v is not None
        }
        for col in df.columns
    ]
    return table_columns, column_formats, df
