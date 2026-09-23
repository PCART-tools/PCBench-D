@deprecate_nonkeyword_arguments()
@deprecated_alias(file="source")
def read_avro(
    source: str | Path | BytesIO | BinaryIO,
    columns: list[int] | list[str] | None = None,
    n_rows: int | None = None,
) -> DataFrame:
    """
    Read into a DataFrame from Apache Avro format.

    Parameters
    ----------
    source
        Path to a file or a file-like object.
    columns
        Columns to select. Accepts a list of column indices (starting at zero) or a list
        of column names.
    n_rows
        Stop reading from Apache Avro file after reading ``n_rows``.

    Returns
    -------
    DataFrame

    """
    return DataFrame._read_avro(source, n_rows=n_rows, columns=columns)
