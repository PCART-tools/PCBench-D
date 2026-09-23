def _read_spreadsheet_ods(
    parser: Any,
    sheet_id: int | None,
    sheet_name: str | None,
    read_csv_options: dict[str, Any] | None,
    schema_overrides: SchemaDict | None,
    *,
    raise_if_empty: bool,
) -> pl.DataFrame:
    """Use the 'ezodf' library to read data from the given worksheet."""
    sheets = parser.sheets
    if sheet_id is not None:
        ws = sheets[sheet_id - 1]
    elif sheet_name is not None:
        ws = next((s for s in sheets if s.name == sheet_name), None)
        if ws is None:
            raise ValueError(f"Sheet {sheet_name!r} not found")
    else:
        ws = sheets[0]

    row_data = []
    found_row_data = False
    for row in ws.rows():
        row_values = [c.value for c in row]
        if found_row_data or (found_row_data := any(v is not None for v in row_values)):
            row_data.append(row_values)

    overrides = {}
    strptime_cols = {}
    headers: list[str] = []

    if not row_data:
        df = pl.DataFrame()
    else:
        for idx, name in enumerate(row_data[0]):
            headers.append(name or (f"_duplicated_{idx}" if headers else ""))

        trailing_null_row = all(v is None for v in row_data[-1])
        row_data = row_data[1 : -1 if trailing_null_row else None]

        if schema_overrides:
            for nm, dtype in schema_overrides.items():
                if dtype in (Datetime, Date):
                    strptime_cols[nm] = dtype
                else:
                    overrides[nm] = dtype

        df = pl.DataFrame(
            row_data,
            orient="row",
            schema=headers,
            schema_overrides=overrides,
        )
    if raise_if_empty and len(df) == 0 and len(df.columns) == 0:
        raise NoDataError(
            "Empty Excel sheet; if you want to read this as "
            "an empty DataFrame, set `raise_if_empty=False`"
        )

    if strptime_cols:
        df = df.with_columns(
            F.col(nm).str.strptime(dtype)  # type: ignore[arg-type]
            for nm, dtype in strptime_cols.items()
        )

    df.columns = headers
    return _drop_unnamed_null_columns(df)
