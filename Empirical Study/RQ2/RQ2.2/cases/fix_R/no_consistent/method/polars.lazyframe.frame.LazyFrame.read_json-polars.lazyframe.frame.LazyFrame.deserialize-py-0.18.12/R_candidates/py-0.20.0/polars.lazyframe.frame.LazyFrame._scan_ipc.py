    @classmethod
    def _scan_ipc(
        cls,
        source: str | Path | list[str] | list[Path],
        *,
        n_rows: int | None = None,
        cache: bool = True,
        rechunk: bool = True,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        storage_options: dict[str, object] | None = None,
        memory_map: bool = True,
    ) -> Self:
        """
        Lazily read from an Arrow IPC (Feather v2) file.

        Use `pl.scan_ipc` to dispatch to this method.

        See Also
        --------
        polars.io.scan_ipc

        """
        if isinstance(source, (str, Path)):
            can_use_fsspec = True
            source = normalize_filepath(source)
            sources = []
        else:
            can_use_fsspec = False
            sources = [normalize_filepath(source) for source in source]
            source = None  # type: ignore[assignment]

        # try fsspec scanner
        if can_use_fsspec and not _is_local_file(source):  # type: ignore[arg-type]
            scan = _scan_ipc_fsspec(source, storage_options)  # type: ignore[arg-type]
            if n_rows:
                scan = scan.head(n_rows)
            if row_count_name is not None:
                scan = scan.with_row_count(row_count_name, row_count_offset)
            return scan  # type: ignore[return-value]

        self = cls.__new__(cls)
        self._ldf = PyLazyFrame.new_from_ipc(
            source,
            sources,
            n_rows,
            cache,
            rechunk,
            _prepare_row_count_args(row_count_name, row_count_offset),
            memory_map=memory_map,
        )
        return self
