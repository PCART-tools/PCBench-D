    @property
    def schema(self) -> OrderedDict[str, DataType]:
        """
        Get a dict[column name, DataType].

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.schema
        OrderedDict({'foo': Int64, 'bar': Float64, 'ham': String})

        """
        return OrderedDict(zip(self.columns, self.dtypes))
