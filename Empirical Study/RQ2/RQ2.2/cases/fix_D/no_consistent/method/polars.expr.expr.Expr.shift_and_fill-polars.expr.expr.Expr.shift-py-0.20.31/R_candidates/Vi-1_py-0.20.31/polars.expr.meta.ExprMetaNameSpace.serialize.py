    def serialize(self, file: IOBase | str | Path | None = None) -> str | None:
        """
        Serialize this expression to a file or string in JSON format.

        Parameters
        ----------
        file
            File path to which the result should be written. If set to `None`
            (default), the output is returned as a string instead.

        See Also
        --------
        Expr.deserialize

        Examples
        --------
        Serialize the expression into a JSON string.

        >>> expr = pl.col("foo").sum().over("bar")
        >>> json = expr.meta.serialize()
        >>> json
        '{"Window":{"function":{"Agg":{"Sum":{"Column":"foo"}}},"partition_by":[{"Column":"bar"}],"options":{"Over":"GroupsToRows"}}}'

        The expression can later be deserialized back into an `Expr` object.

        >>> from io import StringIO
        >>> pl.Expr.deserialize(StringIO(json))  # doctest: +ELLIPSIS
        <Expr ['col("foo").sum().over([col("ba…'] at ...>
        """

        def serialize_to_string() -> str:
            with BytesIO() as buf:
                self._pyexpr.serialize(buf)
                json_bytes = buf.getvalue()
            return json_bytes.decode("utf8")

        if file is None:
            return serialize_to_string()
        elif isinstance(file, StringIO):
            json_str = serialize_to_string()
            file.write(json_str)
            return None
        elif isinstance(file, (str, Path)):
            file = normalize_filepath(file)
            self._pyexpr.serialize(file)
            return None
        else:
            self._pyexpr.serialize(file)
            return None
