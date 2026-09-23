    @property
    def schema(self) -> OrderedDict[str, DataType]:
        """
        Get a dict[column name, DataType].

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.schema
        OrderedDict({'foo': Int64, 'bar': Float64, 'ham': Utf8})

        """
        return OrderedDict(self._ldf.schema())
