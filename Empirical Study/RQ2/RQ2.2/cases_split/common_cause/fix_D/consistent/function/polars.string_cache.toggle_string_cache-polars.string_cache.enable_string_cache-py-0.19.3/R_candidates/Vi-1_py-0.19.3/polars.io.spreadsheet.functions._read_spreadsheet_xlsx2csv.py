def _read_spreadsheet_xlsx2csv(
    parser: Any,
    sheet_id: int | None,
    sheet_name: str | None,
    read_csv_options: dict[str, Any] | None,
    schema_overrides: SchemaDict | None,
    *,
    raise_if_empty: bool,
) -> pl.DataFrame:
    """Use the 'xlsx2csv' library to read data from the given worksheet."""
    csv_buffer = StringIO()
    parser.convert(
        outfile=csv_buffer,
        sheetid=sheet_id,
        sheetname=sheet_name,
    )
    return _csv_buffer_to_frame(
        csv_buffer,
        separator=",",
        read_csv_options=read_csv_options,
        schema_overrides=schema_overrides,
        raise_if_empty=raise_if_empty,
    )
