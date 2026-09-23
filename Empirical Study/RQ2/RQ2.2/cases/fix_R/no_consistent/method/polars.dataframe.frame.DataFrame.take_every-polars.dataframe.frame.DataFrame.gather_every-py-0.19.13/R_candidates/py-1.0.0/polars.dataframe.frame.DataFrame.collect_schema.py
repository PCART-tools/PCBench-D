    def collect_schema(self) -> Schema:
        """
        Get an ordered mapping of column names to their data type.

        This is an alias for the :attr:`schema` property.

        See Also
        --------
        schema

        Notes
        -----
        This method is included to facilitate writing code that is generic for both
        DataFrame and LazyFrame.

        Examples
        --------
        Determine the schema.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.collect_schema()
        Schema({'foo': Int64, 'bar': Float64, 'ham': String})

        Access various properties of the schema using the :class:`Schema` object.

        >>> schema = df.collect_schema()
        >>> schema["bar"]
        Float64
        >>> schema.names()
        ['foo', 'bar', 'ham']
        >>> schema.dtypes()
        [Int64, Float64, String]
        >>> schema.len()
        3
        """
        return self.schema
