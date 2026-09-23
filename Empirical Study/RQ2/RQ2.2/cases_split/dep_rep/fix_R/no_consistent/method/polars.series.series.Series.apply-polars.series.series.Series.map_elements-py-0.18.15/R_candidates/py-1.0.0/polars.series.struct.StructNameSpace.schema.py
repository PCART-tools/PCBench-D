    @property
    def schema(self) -> Schema:
        """
        Get the struct definition as a name/dtype schema dict.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.schema
        Schema({'a': Int64, 'b': Int64})
        """
        if getattr(self, "_s", None) is None:
            return Schema({})

        schema = self._s.dtype().to_schema()
        return Schema(schema)
