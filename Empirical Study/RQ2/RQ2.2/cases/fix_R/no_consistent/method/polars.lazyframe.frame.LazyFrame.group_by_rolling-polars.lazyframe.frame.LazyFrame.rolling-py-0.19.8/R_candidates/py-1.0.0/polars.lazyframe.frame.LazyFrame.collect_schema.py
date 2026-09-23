    def collect_schema(self) -> Schema:
        """
        Resolve the schema of this LazyFrame.

        Examples
        --------
        Determine the schema.

        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.collect_schema()
        Schema({'foo': Int64, 'bar': Float64, 'ham': String})

        Access various properties of the schema.

        >>> schema = lf.collect_schema()
        >>> schema["bar"]
        Float64
        >>> schema.names()
        ['foo', 'bar', 'ham']
        >>> schema.dtypes()
        [Int64, Float64, String]
        >>> schema.len()
        3
        """
        return Schema(self._ldf.collect_schema())
