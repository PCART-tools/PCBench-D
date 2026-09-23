    @classmethod
    def _read_ipc_stream(
        cls,
        source: str | Path | IO[bytes] | bytes,
        *,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
        row_count_name: str | None = None,
        row_count_offset: int = 0,
        rechunk: bool = True,
    ) -> Self:
        """
        Read into a DataFrame from Arrow IPC record batch stream format.

        See "Streaming format" on https://arrow.apache.org/docs/python/ipc.html.

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
            Stop reading from IPC stream after reading `n_rows`.
        row_count_name
            Row count name.
        row_count_offset
            Row count offset.
        rechunk
            Make sure that all data is contiguous.

        """
        if isinstance(source, (str, Path)):
            source = normalize_filepath(source)
        if isinstance(columns, str):
            columns = [columns]

        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_ipc_stream(
            source,
            columns,
            projection,
            n_rows,
            _prepare_row_count_args(row_count_name, row_count_offset),
            rechunk,
        )
        return self
