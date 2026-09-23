@deprecated_alias(file="source")
def read_ipc_schema(source: str | BinaryIO | Path | bytes) -> dict[str, PolarsDataType]:
    """
    Get the schema of an IPC file without reading data.

    Parameters
    ----------
    source
        Path to a file or a file-like object.

    Returns
    -------
    Dictionary mapping column names to datatypes

    """
    if isinstance(source, (str, Path)):
        source = normalise_filepath(source)

    return _ipc_schema(source)
