    @classmethod
    def _read_avro(
        cls,
        source: str | Path | BinaryIO | bytes,
        *,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
    ) -> Self:
        """
        Read into a DataFrame from Apache Avro format.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).
        columns
            Columns.
        n_rows
            Stop reading from Apache Avro file after reading `n_rows`.

        """
        if isinstance(source, (str, Path)):
            source = normalize_filepath(source)
        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_avro(source, columns, projection, n_rows)
        return self
