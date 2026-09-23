def _read_spreadsheet_pyxlsb(
    parser: Any,
    sheet_name: str | None,
    read_csv_options: dict[str, Any] | None,
    schema_overrides: SchemaDict | None,
    *,
    raise_if_empty: bool,
) -> pl.DataFrame:
    from pyxlsb import convert_date

    ws = parser.get_sheet(sheet_name)
    try:
        # establish header/data rows
        header: list[str | None] = []
        rows_iter = ws.rows()
        for row in rows_iter:
            row_values = [cell.v for cell in row]
            if any(v is not None for v in row_values):
                header.extend(row_values)
                break

        # load data rows as series
        series_data = [
            pl.Series(name, [cell.v for cell in column_data])
            for name, column_data in zip(header, zip(*rows_iter))
            if name
        ]
    finally:
        ws.close()

    if schema_overrides:
        for idx, s in enumerate(series_data):
            if schema_overrides.get(s.name) in (Datetime, Date):
                series_data[idx] = s.map_elements(convert_date)

    df = pl.DataFrame(
        {s.name: s for s in series_data},
        schema_overrides=schema_overrides,
    )
    if raise_if_empty and len(df) == 0 and len(df.columns) == 0:
        raise NoDataError(
            "Empty Excel sheet; if you want to read this as "
            "an empty DataFrame, set `raise_if_empty=False`"
        )
    return _drop_unnamed_null_columns(df)
