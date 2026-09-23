def read_parquet_schema(
    source: str | BinaryIO | Path | bytes,
) -> dict[str, PolarsDataType]:
    """
    Get the schema of a Parquet file without reading data.

    Parameters
    ----------
    source
        Path to a file or a file-like object (by file-like object, we refer to objects
        that have a ``read()`` method, such as a file handler (e.g. via builtin ``open``
        function) or ``BytesIO``).

    Returns
    -------
    dict
        Dictionary mapping column names to datatypes

    """
    if isinstance(source, (str, Path)):
        source = normalize_filepath(source)

    return _read_parquet_schema(source)
