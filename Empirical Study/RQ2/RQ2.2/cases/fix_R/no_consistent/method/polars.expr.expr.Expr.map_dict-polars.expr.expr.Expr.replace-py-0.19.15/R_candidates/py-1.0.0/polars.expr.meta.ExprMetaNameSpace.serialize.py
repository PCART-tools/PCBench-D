    def serialize(
        self,
        file: IOBase | str | Path | None = None,
        *,
        format: SerializationFormat = "binary",
    ) -> bytes | str | None:
        r"""
        Serialize this expression to a file or string in JSON format.

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
        Expr.deserialize

        Notes
        -----
        Serialization is not stable across Polars versions: a LazyFrame serialized
        in one Polars version may not be deserializable in another Polars version.

        Examples
        --------
        Serialize the expression into a binary representation.

        >>> expr = pl.col("foo").sum().over("bar")
        >>> bytes = expr.meta.serialize()
        >>> bytes  # doctest: +ELLIPSIS
        b'\xa1fWindow\xa4hfunction\xa1cAgg\xa1cSum\xa1fColumncfoolpartition_by\x81...'

        The bytes can later be deserialized back into an `Expr` object.

        >>> import io
        >>> pl.Expr.deserialize(io.BytesIO(bytes))  # doctest: +ELLIPSIS
        <Expr ['col("foo").sum().over([col("ba…'] at ...>
        """
        if format == "binary":
            serializer = self._pyexpr.serialize_binary
        elif format == "json":
            serializer = self._pyexpr.serialize_json
        else:
            msg = f"`format` must be one of {{'binary', 'json'}}, got {format!r}"
            raise ValueError(msg)

        return serialize_polars_object(serializer, file, format)
