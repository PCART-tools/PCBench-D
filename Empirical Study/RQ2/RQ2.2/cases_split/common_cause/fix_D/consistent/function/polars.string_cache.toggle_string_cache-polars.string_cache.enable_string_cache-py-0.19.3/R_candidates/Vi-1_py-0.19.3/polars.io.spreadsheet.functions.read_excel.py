def read_excel(
    source: str | BytesIO | Path | BinaryIO | bytes,
    *,
    sheet_id: int | Sequence[int] | None = None,
    sheet_name: str | list[str] | tuple[str] | None = None,
    engine: Literal["xlsx2csv", "openpyxl"] | None = None,
    xlsx2csv_options: dict[str, Any] | None = None,
    read_csv_options: dict[str, Any] | None = None,
    schema_overrides: SchemaDict | None = None,
    raise_if_empty: bool = True,
) -> pl.DataFrame | dict[str, pl.DataFrame]:
    """
    Read Excel (XLSX) spreadsheet data into a DataFrame.

    If using the ``xlsx2csv`` engine, converts an Excel sheet with
    ``xlsx2csv.Xlsx2csv().convert()`` to CSV and parses the CSV output with
    :func:`read_csv`. You can pass additional options to ``read_csv_options`` to
    influence parsing behaviour.

    When using the ``openpyxl`` engine, reads an Excel sheet with
    ``openpyxl.load_workbook(source)``.

    Parameters
    ----------
    source
        Path to a file or a file-like object (by file-like object, we refer to objects
        that have a ``read()`` method, such as a file handler (e.g. via builtin ``open``
        function) or ``BytesIO``).
    sheet_id
        Sheet number(s) to convert (set ``0`` to load all sheets as DataFrames) and
        return a ``{sheetname:frame,}`` dict. (Defaults to `1` if neither this nor
        `sheet_name` are specified). Can also take a sequence of sheet numbers.
    sheet_name
        Sheet name(s) to convert; cannot be used in conjunction with `sheet_id`. If more
        than one is given then a ``{sheetname:frame,}`` dict is returned.
    engine
        Library used to parse the spreadsheet file; defaults to "xlsx2csv" if not set.

        * "xlsx2csv": the fastest engine; converts the data to an in-memory CSV first
          and then uses the polars ``read_csv`` method to parse the result. You can
          pass `xlsx2csv_options` and/or `read_csv_options` to refine the conversion.
        * "openpyxl": slower than ``xlsx2csv`` but supports additional automatic type
          inference; potentially useful if you are unable to parse your sheet with
          the ``xlsx2csv`` engine.
        * "odf": this engine is only used for OpenOffice files; it will be used
          automatically for files with the ".ods" extension.
    xlsx2csv_options
        Extra options passed to ``xlsx2csv.Xlsx2csv()``,
        e.g. ``{"skip_empty_lines": True}``
    read_csv_options
        Extra options passed to :func:`read_csv` for parsing the CSV file returned by
        ``xlsx2csv.Xlsx2csv().convert()``
        e.g.: ``{"has_header": False, "new_columns": ["a", "b", "c"],
        "infer_schema_length": None}``
    schema_overrides
        Support type specification or override of one or more columns.
    raise_if_empty
        When there is no data in the sheet,``NoDataError`` is raised. If this parameter
        is set to False, an empty DataFrame (with no columns) is returned instead.

    Returns
    -------
    DataFrame, or a ``{sheetname: DataFrame, ...}`` dict if reading multiple sheets.

    Examples
    --------
    Read the "data" worksheet from an Excel file into a DataFrame.

    >>> pl.read_excel(
    ...     source="test.xlsx",
    ...     sheet_name="data",
    ... )  # doctest: +SKIP

    Read table data from sheet 3 in an Excel workbook as a DataFrame while skipping
    empty lines in the sheet. As sheet 3 does not have a header row and the default
    engine is ``xlsx2csv`` you can pass the necessary additional settings for this
    to the "read_csv_options" parameter; these will be passed to :func:`read_csv`.

    >>> pl.read_excel(
    ...     source="test.xlsx",
    ...     sheet_id=3,
    ...     xlsx2csv_options={"skip_empty_lines": True},
    ...     read_csv_options={"has_header": False, "new_columns": ["a", "b", "c"]},
    ... )  # doctest: +SKIP

    If the correct datatypes can't be determined you can use ``schema_overrides`` and/or
    some of the :func:`read_csv` documentation to see which options you can pass to fix
    this issue. For example ``"infer_schema_length": None`` can be used to read the
    data twice, once to infer the correct output types and once more to then read the
    data with those types. If the types are known in advance then ``schema_overrides``
    is the more efficient option.

    >>> pl.read_excel(
    ...     source="test.xlsx",
    ...     read_csv_options={"infer_schema_length": 1000},
    ...     schema_overrides={"dt": pl.Date},
    ... )  # doctest: +SKIP

    The ``openpyxl`` package can also be used to parse Excel data; it has slightly
    better default type detection, but is slower than ``xlsx2csv``. If you have a sheet
    that is better read using this package you can set the engine as "openpyxl" (if you
    use this engine then both `xlsx2csv_options` and `read_csv_options` cannot be set).

    >>> pl.read_excel(
    ...     source="test.xlsx",
    ...     engine="openpyxl",
    ...     schema_overrides={"dt": pl.Datetime, "value": pl.Int32},
    ... )  # doctest: +SKIP

    """
    if xlsx2csv_options is None:
        xlsx2csv_options = {}

    if read_csv_options is None:
        read_csv_options = {"truncate_ragged_lines": True}
    elif "truncate_ragged_lines" not in read_csv_options:
        read_csv_options["truncate_ragged_lines"] = True

    return _read_spreadsheet(
        sheet_id,
        sheet_name,
        source=source,
        engine=engine,
        engine_options=xlsx2csv_options,
        read_csv_options=read_csv_options,
        schema_overrides=schema_overrides,
        raise_if_empty=raise_if_empty,
    )
