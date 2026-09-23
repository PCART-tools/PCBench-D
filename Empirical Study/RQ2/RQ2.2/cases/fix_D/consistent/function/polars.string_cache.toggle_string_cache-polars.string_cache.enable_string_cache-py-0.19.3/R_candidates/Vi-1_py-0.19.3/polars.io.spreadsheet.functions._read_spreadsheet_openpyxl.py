def _read_spreadsheet_openpyxl(
    parser: Any,
    sheet_id: int | None,
    sheet_name: str | None,
    read_csv_options: dict[str, Any] | None,
    schema_overrides: SchemaDict | None,
    *,
    raise_if_empty: bool,
) -> pl.DataFrame:
    """Use the 'openpyxl' library to read data from the given worksheet."""
    # read requested sheet if provided on kwargs, otherwise read active sheet
    if sheet_name is not None:
        ws = parser[sheet_name]
    elif sheet_id is not None:
        ws = parser.worksheets[sheet_id - 1]
    else:
        ws = parser.active

    # prefer detection of actual table objects; otherwise read
    # data in the used worksheet range, dropping null columns
    header: list[str | None] = []
    if tables := getattr(ws, "tables", None):
        table = next(iter(tables.values()))
        rows = list(ws[table.ref])
        header.extend(cell.value for cell in rows.pop(0))
        if table.totalsRowCount:
            rows = rows[: -table.totalsRowCount]
        rows_iter = iter(rows)
    else:
        rows_iter = ws.iter_rows()
        for row in rows_iter:
            row_values = [cell.value for cell in row]
            if any(v is not None for v in row_values):
                header.extend(row_values)
                break

    series_data = [
        pl.Series(name, [cell.value for cell in column_data])
        for name, column_data in zip(header, zip(*rows_iter))
    ]
    df = pl.DataFrame(
        {s.name: s for s in series_data if s.name},
        schema_overrides=schema_overrides,
    )
    if raise_if_empty and len(df) == 0 and len(df.columns) == 0:
        raise NoDataError(
            "Empty Excel sheet; if you want to read this as "
            "an empty DataFrame, set `raise_if_empty=False`"
        )
    return _drop_unnamed_null_columns(df)
