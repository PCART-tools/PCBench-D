def _csv_buffer_to_frame(
    csv: StringIO,
    separator: str,
    read_csv_options: dict[str, Any] | None,
    schema_overrides: SchemaDict | None,
    *,
    raise_if_empty: bool,
) -> pl.DataFrame:
    """Translate StringIO buffer containing delimited data as a DataFrame."""
    # handle (completely) empty sheet data
    if csv.tell() == 0:
        if raise_if_empty:
            raise NoDataError(
                "Empty Excel sheet; if you want to read this as "
                "an empty DataFrame, set `raise_if_empty=False`"
            )
        return pl.DataFrame()

    # otherwise rewind the buffer and parse as csv
    csv.seek(0)
    df = read_csv(
        csv,
        separator=separator,
        dtypes=schema_overrides,
        **(read_csv_options or {}),
    )
    return _drop_unnamed_null_columns(df)
