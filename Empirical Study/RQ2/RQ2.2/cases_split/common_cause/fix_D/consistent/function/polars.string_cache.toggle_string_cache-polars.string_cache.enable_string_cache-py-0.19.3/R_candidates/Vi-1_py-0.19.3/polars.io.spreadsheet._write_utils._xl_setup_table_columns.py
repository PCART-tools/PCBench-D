def _xl_setup_table_columns(
    df: DataFrame,
    format_cache: _XLFormatCache,
    column_totals: ColumnTotalsDefinition | None = None,
    column_formats: ColumnFormatDict | None = None,
    dtype_formats: dict[OneOrMoreDataTypes, str] | None = None,
    header_format: dict[str, Any] | None = None,
    sparklines: dict[str, Sequence[str] | dict[str, Any]] | None = None,
    formulas: dict[str, str | dict[str, str]] | None = None,
    row_totals: RowTotalsDefinition | None = None,
    float_precision: int = 3,
) -> tuple[list[dict[str, Any]], dict[str | tuple[str, ...], str], DataFrame]:
    """Setup and unify all column-related formatting/defaults."""

    # no excel support for compound types; cast to their simple string representation
    def _map_str(s: Series) -> Series:
        return s.__class__(s.name, [str(v) for v in s.to_list()])

    cast_cols = [
        F.col(col).map_batches(_map_str).alias(col)
        for col, tp in df.schema.items()
        if tp in (List, Struct, Object)
    ]
    if cast_cols:
        df = df.with_columns(cast_cols)

    column_totals = _unpack_multi_column_dict(  # type: ignore[assignment]
        _expand_selector_dicts(df, column_totals, expand_keys=True, expand_values=False)
        if isinstance(column_totals, dict)
        else _expand_selectors(df, column_totals)
    )
    column_formats = _unpack_multi_column_dict(  # type: ignore[assignment]
        _expand_selector_dicts(
            df, column_formats, expand_keys=True, expand_values=False, tuple_keys=True
        )
    )

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
                else (
                    {row_totals}
                    if isinstance(row_totals, str)
                    else set(_expand_selectors(df, row_totals))
                )
            )
            n_ucase = sum((c[0] if c else "").isupper() for c in df.columns)
            total = f"{'T' if (n_ucase > len(df.columns) // 2) else 't'}otal"
            row_total_funcs = {total: _xl_table_formula(df, sum_cols, "sum")}
        else:
            row_totals = _expand_selector_dicts(
                df, row_totals, expand_keys=False, expand_values=True
            )
            row_total_funcs = {
                name: _xl_table_formula(
                    df, numeric_cols if cols is True else cols, "sum"
                )
                for name, cols in row_totals.items()
            }

    # normalise formulas
    column_formulas = {
        col: {"formula": options} if isinstance(options, str) else options
        for col, options in (formulas or {}).items()
    }

    # normalise formats
    column_formats = dict(column_formats or {})
    dtype_formats = dict(dtype_formats or {})

    for tp in list(dtype_formats):
        if isinstance(tp, (tuple, frozenset)):
            dtype_formats.update(dict.fromkeys(tp, dtype_formats.pop(tp)))
    for fmt in dtype_formats.values():
        if not isinstance(fmt, str):
            raise TypeError(
                f"invalid dtype_format value: {fmt!r} (expected format string, got {type(fmt).__name__!r})"
            )

    # inject sparkline/row-total placeholder(s)
    if sparklines:
        df = _xl_inject_dummy_table_columns(df, sparklines)
    if column_formulas:
        df = _xl_inject_dummy_table_columns(df, column_formulas)
    if row_totals:
        df = _xl_inject_dummy_table_columns(df, row_total_funcs, dtype=Float64)

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
            elif isinstance(column_totals, str):
                column_total_funcs.setdefault(col, column_totals.lower())
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

    # optional custom header format
    col_header_format = format_cache.get(header_format) if header_format else None

    # assemble table columns
    table_columns = [
        {
            k: v
            for k, v in {
                "header": col,
                "format": column_formats[col],
                "header_format": col_header_format,
                "total_function": column_total_funcs.get(col),
                "formula": (
                    row_total_funcs.get(col)
                    or column_formulas.get(col, {}).get("formula")
                ),
            }.items()
            if v is not None
        }
        for col in df.columns
    ]
    return table_columns, column_formats, df  # type: ignore[return-value]
