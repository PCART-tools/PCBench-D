    @property
    def schema(self) -> SchemaDict:
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
        {'foo': Int64, 'bar': Float64, 'ham': Utf8}

        """
        return dict(zip(self.columns, self.dtypes))
