    @classmethod
    def _read_avro(
        cls: type[DF],
        file: str | Path | BinaryIO,
        columns: Sequence[int] | Sequence[str] | None = None,
        n_rows: int | None = None,
    ) -> DF:
        """
        Read into a DataFrame from Apache Avro format.

        Parameters
        ----------
        file
            Path to a file or a file-like object.
        columns
            Columns.
        n_rows
            Stop reading from Apache Avro file after reading ``n_rows``.

        Returns
        -------
        DataFrame

        """
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)
        projection, columns = handle_projection_columns(columns)
        self = cls.__new__(cls)
        self._df = PyDataFrame.read_avro(file, columns, projection, n_rows)
        return self
