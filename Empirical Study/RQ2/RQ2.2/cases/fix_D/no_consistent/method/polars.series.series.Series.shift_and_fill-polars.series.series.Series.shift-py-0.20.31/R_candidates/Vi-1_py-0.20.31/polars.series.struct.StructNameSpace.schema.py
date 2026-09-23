    @property
    def schema(self) -> OrderedDict[str, DataType]:
        """
        Get the struct definition as a name/dtype schema dict.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.schema
        OrderedDict({'a': Int64, 'b': Int64})
        """
        if getattr(self, "_s", None) is None:
            return OrderedDict()
        return OrderedDict(self._s.dtype().to_schema())
