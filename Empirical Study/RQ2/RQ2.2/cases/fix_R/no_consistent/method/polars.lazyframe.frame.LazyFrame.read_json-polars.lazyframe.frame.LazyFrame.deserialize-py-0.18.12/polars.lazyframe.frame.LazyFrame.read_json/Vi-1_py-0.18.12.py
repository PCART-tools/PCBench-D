    @classmethod
    def read_json(cls, file: str | Path | IOBase) -> Self:
        """
        Read a logical plan from a JSON file to construct a LazyFrame.

        Parameters
        ----------
        file
            Path to a file or a file-like object.

        See Also
        --------
        LazyFrame.from_json, LazyFrame.write_json

        """
        if isinstance(file, StringIO):
            file = BytesIO(file.getvalue().encode())
        elif isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        return cls._from_pyldf(PyLazyFrame.read_json(file))
