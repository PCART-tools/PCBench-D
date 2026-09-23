    @classmethod
    def deserialize(
        cls, source: str | Path | IOBase, *, format: SerializationFormat = "binary"
    ) -> DataFrame:
        """
        Read a serialized DataFrame from a file.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).
        format
            The format with which the DataFrame was serialized. Options:

            - `"binary"`: Deserialize from binary format (bytes). This is the default.
            - `"json"`: Deserialize from JSON format (string).

        See Also
        --------
        DataFrame.serialize

        Notes
        -----
        Serialization is not stable across Polars versions: a LazyFrame serialized
        in one Polars version may not be deserializable in another Polars version.

        Examples
        --------
        >>> import io
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
        >>> bytes = df.serialize()
        >>> pl.DataFrame.deserialize(io.BytesIO(bytes))
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ f64 │
        ╞═════╪═════╡
        │ 1   ┆ 4.0 │
        │ 2   ┆ 5.0 │
        │ 3   ┆ 6.0 │
        └─────┴─────┘
        """
        if isinstance(source, StringIO):
            source = BytesIO(source.getvalue().encode())
        elif isinstance(source, (str, Path)):
            source = normalize_filepath(source)

        if format == "binary":
            deserializer = PyDataFrame.deserialize_binary
        elif format == "json":
            deserializer = PyDataFrame.deserialize_json
        else:
            msg = f"`format` must be one of {{'binary', 'json'}}, got {format!r}"
            raise ValueError(msg)

        return cls._from_pydf(deserializer(source))
