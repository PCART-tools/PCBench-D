    @classmethod
    def _read_json(cls: type[DF], file: str | Path | IOBase) -> DF:
        """
        Read into a DataFrame from a JSON file.

        Use ``pl.read_json`` to dispatch to this method.

        See Also
        --------
        polars.io.read_json

        """
        if isinstance(file, StringIO):
            file = BytesIO(file.getvalue().encode())
        elif isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        self = cls.__new__(cls)
        self._df = PyDataFrame.read_json(file, False)
        return self
