def scan_ipc(
    source: str | Path,
    *,
    n_rows: int | None = None,
    cache: bool = True,
    rechunk: bool = True,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    storage_options: dict[str, Any] | None = None,
    memory_map: bool = True,
) -> LazyFrame:
    """
    Lazily read from an Arrow IPC (Feather v2) file or multiple files via glob patterns.

    This allows the query optimizer to push down predicates and projections to the scan
    level, thereby potentially reducing memory overhead.

    Parameters
    ----------
    source
        Path to a IPC file.
    n_rows
        Stop reading from IPC file after reading ``n_rows``.
    cache
        Cache the result after reading.
    rechunk
        Reallocate to contiguous memory when all chunks/ files are parsed.
    row_count_name
        If not None, this will insert a row count column with give name into the
        DataFrame
    row_count_offset
        Offset to start the row_count column (only use if the name is set)
    storage_options
        Extra options that make sense for ``fsspec.open()`` or a
        particular storage connection.
        e.g. host, port, username, password, etc.
    memory_map
        Try to memory map the file. This can greatly improve performance on repeated
        queries as the OS may cache pages.
        Only uncompressed IPC files can be memory mapped.

    """
    return pl.LazyFrame._scan_ipc(
        source,
        n_rows=n_rows,
        cache=cache,
        rechunk=rechunk,
        row_count_name=row_count_name,
        row_count_offset=row_count_offset,
        storage_options=storage_options,
        memory_map=memory_map,
    )
