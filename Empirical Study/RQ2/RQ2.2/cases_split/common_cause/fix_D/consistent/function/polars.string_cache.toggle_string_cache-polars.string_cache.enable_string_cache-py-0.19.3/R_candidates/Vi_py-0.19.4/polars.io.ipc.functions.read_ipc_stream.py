def read_ipc_stream(
    source: str | BinaryIO | BytesIO | Path | bytes,
    *,
    columns: list[int] | list[str] | None = None,
    n_rows: int | None = None,
    use_pyarrow: bool = False,
    storage_options: dict[str, Any] | None = None,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    rechunk: bool = True,
) -> DataFrame:
    """
    Read into a DataFrame from Arrow IPC record batch stream.

    Parameters
    ----------
    source
        Path to a file or a file-like object (by file-like object, we refer to objects
        that have a ``read()`` method, such as a file handler (e.g. via builtin ``open``
        function) or ``BytesIO``). If ``fsspec`` is installed, it will be used to open
        remote files.
    columns
        Columns to select. Accepts a list of column indices (starting at zero) or a list
        of column names.
    n_rows
        Stop reading from IPC stream after reading ``n_rows``.
        Only valid when `use_pyarrow=False`.
    use_pyarrow
        Use pyarrow or the native Rust reader.
    storage_options
        Extra options that make sense for ``fsspec.open()`` or a particular storage
        connection, e.g. host, port, username, password, etc.
    row_count_name
        If not None, this will insert a row count column with give name into the
        DataFrame
    row_count_offset
        Offset to start the row_count column (only use if the name is set)
    rechunk
        Make sure that all data is contiguous.

    Returns
    -------
    DataFrame

    """
    storage_options = storage_options or {}
    with _prepare_file_arg(source, use_pyarrow=use_pyarrow, **storage_options) as data:
        if use_pyarrow:
            if not _PYARROW_AVAILABLE:
                raise ModuleNotFoundError(
                    "'pyarrow' is required when using"
                    " 'read_ipc_stream(..., use_pyarrow=True)'"
                )

            import pyarrow as pa

            with pa.ipc.RecordBatchStreamReader(data) as reader:
                tbl = reader.read_all()
                df = pl.DataFrame._from_arrow(tbl, rechunk=rechunk)
                if row_count_name is not None:
                    df = df.with_row_count(row_count_name, row_count_offset)
                if n_rows is not None:
                    df = df.slice(0, n_rows)
                return df

        return pl.DataFrame._read_ipc_stream(
            data,
            columns=columns,
            n_rows=n_rows,
            row_count_name=row_count_name,
            row_count_offset=row_count_offset,
            rechunk=rechunk,
        )
