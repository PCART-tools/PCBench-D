    @classmethod
    def _read_ipc(
        cls,
        file: str | Path | BinaryIO,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        rechunk: bool = True,
        memory_map: bool = True,
    ) -> DataFrame:
        """
        Read into a DataFrame from Arrow IPC stream format.

        Arrow IPC is also know as Feather (v2).

        Parameters
        ----------
        file
            Path to a file or a file-like object.
        columns
            Columns to select. Accepts a list of column indices (starting at zero) or a
            list of column names.
        n_rows
            Stop reading from IPC file after reading ``n_rows``.
        row_count_name
            Row count name.
        row_count_offset
            Row count offset.
        rechunk
            Make sure that all data is contiguous.
        memory_map
            Memory map the file

        Returns
        -------
        DataFrame

        """
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(file, str) and "*" in file and pli._is_local_file(file):
            from polars import scan_ipc

            scan = scan_ipc(
                file,
                n_rows=n_rows,
                rechunk=rechunk,
                row_count_name=row_count_name,
                row_count_offset=row_count_offset,
                memory_map=memory_map,
            )
            if columns is None:
                return scan.collect()
            elif is_str_sequence(columns, allow_str=False):
                return scan.select(columns).collect()
            else:
                raise ValueError(
                    "cannot use glob patterns and integer based projection as `columns`"
                    " argument; Use columns: List[str]"
                )

        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_ipc(
            file,
            columns,
            projection,
            n_rows,
            _prepare_row_count_args(row_count_name, row_count_offset),
            memory_map=memory_map,
        )
        return self
