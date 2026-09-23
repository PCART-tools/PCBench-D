def _read_spreadsheet(
    sheet_id: int | Sequence[int] | None,
    sheet_name: str | list[str] | tuple[str] | None,
    source: str | BytesIO | Path | BinaryIO | bytes,
    engine: Literal["xlsx2csv", "openpyxl", "ods"] | None,
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

    if engine_options is None:
        engine_options = {}

    # establish the reading function, parser, and available worksheets
    reader_fn, parser, worksheets = _initialise_spreadsheet_parser(
        engine, source, engine_options
    )

    # use the parser to read data from one or more sheets
    if (
        sheet_id == 0
        or isinstance(sheet_id, Sequence)
        or (sheet_name and not isinstance(sheet_name, str))
    ):
        # read multiple sheets by id
        sheet_ids = sheet_id or ()
        sheet_names = sheet_name or ()
        return {
            sheet["name"]: reader_fn(
                parser=parser,
                sheet_id=sheet["index"],
                sheet_name=None,
                read_csv_options=read_csv_options,
                schema_overrides=schema_overrides,
                raise_if_empty=raise_if_empty,
            )
            for sheet in worksheets
            if sheet_id == 0 or sheet["index"] in sheet_ids or sheet["name"] in sheet_names  # type: ignore[operator]
        }
    else:
        # read a specific sheet by id or name
        if sheet_name is None:
            sheet_id = sheet_id or 1

        return reader_fn(
            parser=parser,
            sheet_id=sheet_id,
            sheet_name=sheet_name,
            read_csv_options=read_csv_options,
            schema_overrides=schema_overrides,
            raise_if_empty=raise_if_empty,
        )
