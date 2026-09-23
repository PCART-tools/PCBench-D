    @classmethod
    def _read_ipc(
        cls,
        source: str | Path | IO[bytes] | bytes,
        *,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        rechunk: bool = True,
        memory_map: bool = True,
    ) -> Self:
        """
        Read into a DataFrame from Arrow IPC file format.

        See "File or Random Access format" on https://arrow.apache.org/docs/python/ipc.html.
        Arrow IPC files are also known as Feather (v2) files.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).
        columns
            Columns to select. Accepts a list of column indices (starting at zero) or a
            list of column names.
        n_rows
            Stop reading from IPC file after reading `n_rows`.
        row_count_name
            Row count name.
        row_count_offset
            Row count offset.
        rechunk
            Make sure that all data is contiguous.
        memory_map
            Memory map the file

        """
        if isinstance(source, (str, Path)):
            source = normalize_filepath(source)
        if isinstance(columns, str):
            columns = [columns]

        if (
            isinstance(source, str)
            and _is_glob_pattern(source)
            and _is_local_file(source)
        ):
            from polars import scan_ipc

            scan = scan_ipc(
                source,
                n_rows=n_rows,
                rechunk=rechunk,
                row_count_name=row_count_name,
                row_count_offset=row_count_offset,
                memory_map=memory_map,
            )
            if columns is None:
                df = scan.collect()
            elif is_str_sequence(columns, allow_str=False):
                df = scan.select(columns).collect()
            else:
                raise TypeError(
                    "cannot use glob patterns and integer based projection as `columns` argument"
                    "\n\nUse columns: List[str]"
                )
            return cls._from_pydf(df._df)

        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_ipc(
            source,
            columns,
            projection,
            n_rows,
            _prepare_row_count_args(row_count_name, row_count_offset),
            memory_map=memory_map,
        )
        return self
