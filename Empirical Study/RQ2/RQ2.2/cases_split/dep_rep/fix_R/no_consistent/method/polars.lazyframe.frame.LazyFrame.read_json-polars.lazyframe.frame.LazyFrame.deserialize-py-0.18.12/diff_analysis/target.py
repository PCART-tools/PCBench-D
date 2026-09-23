    @classmethod
    def deserialize(cls, source: str | Path | IOBase) -> Self:
        """
        Read a logical plan from a JSON file to construct a LazyFrame.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).

        See Also
        --------
        LazyFrame.serialize

        Examples
        --------
        >>> import io
        >>> lf = pl.LazyFrame({"a": [1, 2, 3]}).sum()
        >>> json = lf.serialize()
        >>> pl.LazyFrame.deserialize(io.StringIO(json)).collect()
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 6   │
        └─────┘

        """
        if isinstance(source, StringIO):
            source = BytesIO(source.getvalue().encode())
        elif isinstance(source, (str, Path)):
            source = normalize_filepath(source)

        return cls._from_pyldf(PyLazyFrame.deserialize(source))
