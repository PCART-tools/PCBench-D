def _initialise_spreadsheet_parser(
    engine: Literal["xlsx2csv", "openpyxl", "ods"] | None,
    source: str | BytesIO | Path | BinaryIO | bytes,
    engine_options: dict[str, Any],
) -> tuple[Callable[..., pl.DataFrame], Any, list[dict[str, Any]]]:
    """Instantiate the indicated spreadsheet parser and establish related properties."""
    if isinstance(source, (str, Path)):
        source = normalize_filepath(source)
    if engine is None and str(source).lower().endswith(".ods"):
        engine = "ods"

    if engine == "xlsx2csv" or engine is None:  # default
        try:
            import xlsx2csv
        except ImportError:
            raise ModuleNotFoundError(
                "Required package not installed\n\nPlease run: `pip install xlsx2csv`"
            ) from None
        parser = xlsx2csv.Xlsx2csv(source, **engine_options)
        sheets = parser.workbook.sheets
        return _read_spreadsheet_xlsx2csv, parser, sheets

    elif engine == "openpyxl":
        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                "Required package not installed\n\nPlease run `pip install openpyxl`"
            ) from None
        parser = openpyxl.load_workbook(source, data_only=True, **engine_options)
        sheets = [{"index": i + 1, "name": ws.title} for i, ws in enumerate(parser)]
        return _read_spreadsheet_openpyxl, parser, sheets

    elif engine == "ods":
        try:
            import ezodf
        except ImportError:
            raise ImportError(
                "Required package not installed\n\nPlease run `pip install ezodf lxml`"
            ) from None
        parser = ezodf.opendoc(source, **engine_options)
        sheets = [
            {"index": i + 1, "name": ws.name} for i, ws in enumerate(parser.sheets)
        ]
        return _read_spreadsheet_ods, parser, sheets

    raise NotImplementedError(f"Unrecognised engine: {engine!r}")
