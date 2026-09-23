    @classmethod
    def _read_parquet(
        cls,
        source: str | Path | IO[bytes] | bytes,
        *,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
        parallel: ParallelStrategy = "auto",
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        low_memory: bool = False,
        use_statistics: bool = True,
        rechunk: bool = True,
    ) -> DataFrame:
        """
        Read into a DataFrame from a parquet file.

        Use `pl.read_parquet` to dispatch to this method.

        See Also
        --------
        polars.io.read_parquet

        """
        if isinstance(source, (str, Path)):
            source = normalize_filepath(source)
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(source, str) and _is_glob_pattern(source):
            from polars import scan_parquet

            scan = scan_parquet(
                source,
                n_rows=n_rows,
                rechunk=True,
                parallel=parallel,
                row_count_name=row_count_name,
                row_count_offset=row_count_offset,
                low_memory=low_memory,
            )

            if columns is None:
                return scan.collect()
            elif is_str_sequence(columns, allow_str=False):
                return scan.select(columns).collect()
            else:
                raise TypeError(
                    "cannot use glob patterns and integer based projection as `columns` argument"
                    "\n\nUse columns: List[str]"
                )

        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_parquet(
            source,
            columns,
            projection,
            n_rows,
            parallel,
            _prepare_row_count_args(row_count_name, row_count_offset),
            low_memory=low_memory,
            use_statistics=use_statistics,
            rechunk=rechunk,
        )
        return self
