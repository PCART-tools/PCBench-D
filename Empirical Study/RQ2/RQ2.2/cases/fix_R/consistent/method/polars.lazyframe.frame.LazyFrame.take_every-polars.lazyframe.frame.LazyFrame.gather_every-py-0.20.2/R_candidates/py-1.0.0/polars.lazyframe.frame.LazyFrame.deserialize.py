    @classmethod
    def deserialize(
        cls, source: str | Path | IOBase, *, format: SerializationFormat = "binary"
    ) -> LazyFrame:
        """
        Read a logical plan from a file to construct a LazyFrame.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).
        format
            The format with which the LazyFrame was serialized. Options:

            - `"binary"`: Deserialize from binary format (bytes). This is the default.
            - `"json"`: Deserialize from JSON format (string).

        Warnings
        --------
        This function uses :mod:`pickle` if the logical plan contains Python UDFs,
        and as such inherits the security implications. Deserializing can execute
        arbitrary code, so it should only be attempted on trusted data.

        See Also
        --------
        LazyFrame.serialize

        Notes
        -----
        Serialization is not stable across Polars versions: a LazyFrame serialized
        in one Polars version may not be deserializable in another Polars version.

        Examples
        --------
        >>> import io
        >>> lf = pl.LazyFrame({"a": [1, 2, 3]}).sum()
        >>> bytes = lf.serialize()
        >>> pl.LazyFrame.deserialize(io.BytesIO(bytes)).collect()
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

        if format == "binary":
            deserializer = PyLazyFrame.deserialize_binary
        elif format == "json":
            deserializer = PyLazyFrame.deserialize_json
        else:
            msg = f"`format` must be one of {{'binary', 'json'}}, got {format!r}"
            raise ValueError(msg)

        return cls._from_pyldf(deserializer(source))
