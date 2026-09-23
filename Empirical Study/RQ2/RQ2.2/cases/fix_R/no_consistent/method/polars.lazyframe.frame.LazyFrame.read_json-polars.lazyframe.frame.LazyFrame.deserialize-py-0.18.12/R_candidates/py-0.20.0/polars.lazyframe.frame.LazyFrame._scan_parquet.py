    @classmethod
    def _scan_parquet(
        cls,
        source: str | list[str] | list[Path],
        *,
        n_rows: int | None = None,
        cache: bool = True,
        parallel: ParallelStrategy = "auto",
        rechunk: bool = True,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        storage_options: dict[str, object] | None = None,
        low_memory: bool = False,
        use_statistics: bool = True,
        hive_partitioning: bool = True,
        retries: int = 0,
    ) -> Self:
        """
        Lazily read from a parquet file or multiple files via glob patterns.

        Use `pl.scan_parquet` to dispatch to this method.

        See Also
        --------
        polars.io.scan_parquet

        """
        if isinstance(source, list):
            sources = source
            source = None  # type: ignore[assignment]
            can_use_fsspec = False
        else:
            can_use_fsspec = True
            sources = []

        # try fsspec scanner
        if (
            can_use_fsspec
            and not _is_local_file(source)  # type: ignore[arg-type]
            and not _is_supported_cloud(source)  # type: ignore[arg-type]
        ):
            scan = _scan_parquet_fsspec(source, storage_options)  # type: ignore[arg-type]
            if n_rows:
                scan = scan.head(n_rows)
            if row_count_name is not None:
                scan = scan.with_row_count(row_count_name, row_count_offset)
            return scan  # type: ignore[return-value]

        if storage_options:
            storage_options = list(storage_options.items())  #  type: ignore[assignment]
        else:
            # Handle empty dict input
            storage_options = None

        self = cls.__new__(cls)
        self._ldf = PyLazyFrame.new_from_parquet(
            source,
            sources,
            n_rows,
            cache,
            parallel,
            rechunk,
            _prepare_row_count_args(row_count_name, row_count_offset),
            low_memory,
            cloud_options=storage_options,
            use_statistics=use_statistics,
            hive_partitioning=hive_partitioning,
            retries=retries,
        )
        return self
