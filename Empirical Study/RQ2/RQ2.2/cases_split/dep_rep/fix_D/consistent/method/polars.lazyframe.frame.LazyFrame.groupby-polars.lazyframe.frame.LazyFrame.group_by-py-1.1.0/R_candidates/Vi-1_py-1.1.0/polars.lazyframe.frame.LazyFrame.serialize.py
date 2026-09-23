    def serialize(
        self,
        file: IOBase | str | Path | None = None,
        *,
        format: SerializationFormat = "binary",
    ) -> bytes | str | None:
        r"""
        Serialize the logical plan of this LazyFrame to a file or string in JSON format.

        Parameters
        ----------
        file
            File path to which the result should be written. If set to `None`
            (default), the output is returned as a string instead.
        format
            The format in which to serialize. Options:

            - `"binary"`: Serialize to binary format (bytes). This is the default.
            - `"json"`: Serialize to JSON format (string).

        See Also
        --------
        LazyFrame.deserialize

        Notes
        -----
        Serialization is not stable across Polars versions: a LazyFrame serialized
        in one Polars version may not be deserializable in another Polars version.

        Examples
        --------
        Serialize the logical plan into a binary representation.

        >>> lf = pl.LazyFrame({"a": [1, 2, 3]}).sum()
        >>> bytes = lf.serialize()
        >>> bytes  # doctest: +ELLIPSIS
        b'\xa1kMapFunction\xa2einput\xa1mDataFrameScan\xa4bdf\xa1gcolumns\x81\xa4d...'

        The bytes can later be deserialized back into a LazyFrame.

        >>> import io
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
        if format == "binary":
            serializer = self._ldf.serialize_binary
        elif format == "json":
            serializer = self._ldf.serialize_json
        else:
            msg = f"`format` must be one of {{'binary', 'json'}}, got {format!r}"
            raise ValueError(msg)

        return serialize_polars_object(serializer, file, format)
