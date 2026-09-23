def _read_spreadsheet(
    sheet_id: int | Sequence[int] | None,
    sheet_name: str | list[str] | tuple[str] | None,
    source: str | BytesIO | Path | BinaryIO | bytes,
    engine: Literal["xlsx2csv", "openpyxl", "pyxlsb", "ods"] | None,
    engine_options: dict[str, Any] | None = None,
    read_csv_options: dict[str, Any] | None = None,
    schema_overrides: SchemaDict | None = None,
    *,
    raise_if_empty: bool = True,
) -> pl.DataFrame | dict[str, pl.DataFrame]:
    if sheet_id is not None and sheet_name is not None:
        raise ValueError(
            f"cannot specify both `sheet_name` ({sheet_name!r}) and `sheet_id` ({sheet_id!r})"
        )

    # establish the reading function, parser, and available worksheets
    reader_fn, parser, worksheets = _initialise_spreadsheet_parser(
        engine, source, engine_options or {}
    )

    # determine which named worksheets to read
    if sheet_id is None and sheet_name is None:
        sheet_names = [worksheets[0]["name"]]
        return_multi = False
    else:
        return_multi = (
            sheet_id == 0
            or isinstance(sheet_id, Sequence)
            or (isinstance(sheet_name, Sequence) and not isinstance(sheet_name, str))
        )
        ids = (sheet_id,) if isinstance(sheet_id, int) else sheet_id or ()
        names = (sheet_name,) if isinstance(sheet_name, str) else sheet_name or ()
        sheet_names = [
            ws["name"]
            for ws in worksheets
            if (sheet_id == 0 or ws["index"] in ids or ws["name"] in names)
        ]

    # read data from the indicated sheet(s)
    try:
        parsed_sheets = {
            name: reader_fn(
                parser=parser,
                sheet_name=name,
                read_csv_options=read_csv_options,
                schema_overrides=schema_overrides,
                raise_if_empty=raise_if_empty,
            )
            for name in sheet_names
        }
    finally:
        if hasattr(parser, "close"):
            parser.close()

    if return_multi:
        return parsed_sheets
    return next(iter(parsed_sheets.values()))
