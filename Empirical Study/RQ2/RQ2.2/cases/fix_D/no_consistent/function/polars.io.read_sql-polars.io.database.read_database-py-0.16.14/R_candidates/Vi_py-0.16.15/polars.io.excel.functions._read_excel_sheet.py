def _read_excel_sheet(
    parser: Any,
    sheet_id: int | None,
    sheet_name: str | None,
    read_csv_options: dict[str, Any],
) -> DataFrame:
    csv_buffer = StringIO()

    # Parse XLSX sheet to CSV.
    parser.convert(outfile=csv_buffer, sheetid=sheet_id, sheetname=sheet_name)

    # Rewind buffer to start.
    csv_buffer.seek(0)

    # Parse CSV output.
    return read_csv(csv_buffer, **read_csv_options)
