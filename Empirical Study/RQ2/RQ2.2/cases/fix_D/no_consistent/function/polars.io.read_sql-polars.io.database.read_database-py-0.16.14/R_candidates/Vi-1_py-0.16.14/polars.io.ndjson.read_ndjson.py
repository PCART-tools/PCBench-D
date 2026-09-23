@deprecated_alias(file="source")
def read_ndjson(source: str | Path | IOBase) -> DataFrame:
    """
    Read into a DataFrame from a newline delimited JSON file.

    Parameters
    ----------
    source
        Path to a file or a file-like object.

    """
    return DataFrame._read_ndjson(source)
