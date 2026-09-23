def scan_parquet(
    source: str | Path,
    *,
    n_rows: int | None = None,
    cache: bool = True,
    parallel: ParallelStrategy = "auto",
    rechunk: bool = True,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    storage_options: dict[str, Any] | None = None,
    low_memory: bool = False,
    use_statistics: bool = True,
) -> LazyFrame:
    """
    Lazily read from a parquet file or multiple files via glob patterns.

    This allows the query optimizer to push down predicates and projections to the scan
    level, thereby potentially reducing memory overhead.

    Notes
    -----
    * Partitioned files:
        If you have a directory-nested (hive-style) partitioned dataset, you should
        use the :func:`scan_pyarrow_dataset` method to read that data instead.

    Parameters
    ----------
    source
        Path to a file.
    n_rows
        Stop reading from parquet file after reading ``n_rows``.
    cache
        Cache the result after reading.
    parallel : {'auto', 'columns', 'row_groups', 'none'}
        This determines the direction of parallelism. 'auto' will try to determine the
        optimal direction.
    rechunk
        In case of reading multiple files via a glob pattern rechunk the final DataFrame
        into contiguous memory chunks.
    row_count_name
        If not None, this will insert a row count column with give name into the
        DataFrame
    row_count_offset
        Offset to start the row_count column (only use if the name is set)
    storage_options
        Extra options that make sense for ``fsspec.open()`` or a
        particular storage connection.
        e.g. host, port, username, password, etc.
    low_memory
        Reduce memory pressure at the expense of performance.
    use_statistics
        Use statistics in the parquet to determine if pages
        can be skipped from reading.

    See Also
    --------
    read_parquet
    scan_pyarrow_dataset

    """
    if isinstance(source, (str, Path)):
        source = normalize_filepath(source)

    return pl.LazyFrame._scan_parquet(
        source,
        n_rows=n_rows,
        cache=cache,
        parallel=parallel,
        rechunk=rechunk,
        row_count_name=row_count_name,
        row_count_offset=row_count_offset,
        storage_options=storage_options,
        low_memory=low_memory,
        use_statistics=use_statistics,
    )
