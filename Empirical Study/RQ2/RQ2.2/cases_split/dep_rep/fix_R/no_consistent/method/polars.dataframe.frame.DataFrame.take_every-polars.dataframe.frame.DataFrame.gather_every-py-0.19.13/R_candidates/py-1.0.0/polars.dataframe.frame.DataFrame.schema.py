    @property
    def schema(self) -> Schema:
        """
        Get an ordered mapping of column names to their data type.

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
        Schema({'foo': Int64, 'bar': Float64, 'ham': String})
        """
        return Schema(zip(self.columns, self.dtypes))
