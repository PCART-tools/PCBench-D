    @classmethod
    def _read_parquet(
        cls: type[DF],
        file: str | Path | BinaryIO,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
        parallel: ParallelStrategy = "auto",
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        low_memory: bool = False,
    ) -> DF:
        """
        Read into a DataFrame from a parquet file.

        Use ``pl.read_parquet`` to dispatch to this method.

        See Also
        --------
        polars.io.read_parquet

        """
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(file, str) and "*" in file and pli._is_local_file(file):
            from polars import scan_parquet

            scan = scan_parquet(
                file,
                n_rows=n_rows,
                rechunk=True,
                parallel=parallel,
                row_count_name=row_count_name,
                row_count_offset=row_count_offset,
                low_memory=low_memory,
            )

            if columns is None:
                return cls._from_pydf(scan.collect()._df)
            elif is_str_sequence(columns, allow_str=False):
                return cls._from_pydf(scan.select(columns).collect()._df)
            else:
                raise ValueError(
                    "cannot use glob patterns and integer based projection as `columns`"
                    " argument; Use columns: List[str]"
                )

        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_parquet(
            file,
            columns,
            projection,
            n_rows,
            parallel,
            _prepare_row_count_args(row_count_name, row_count_offset),
            low_memory=low_memory,
        )
        return self
