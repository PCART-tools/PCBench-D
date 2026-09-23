    @classmethod
    def _read_ndjson(cls: type[DF], file: str | Path | IOBase) -> DF:
        """
        Read into a DataFrame from a newline delimited JSON file.

        Use ``pl.read_ndjson`` to dispatch to this method.

        See Also
        --------
        polars.io.read_ndjson

        """
        if isinstance(file, StringIO):
            file = BytesIO(file.getvalue().encode())
        elif isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        self = cls.__new__(cls)
        self._df = PyDataFrame.read_ndjson(file)
        return self
