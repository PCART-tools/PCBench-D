    @property
    def schema(self) -> Schema:
        """
        Get an ordered mapping of column names to their data type.

        Warnings
        --------
        Resolving the schema of a LazyFrame is a potentially expensive operation.
        Using :meth:`collect_schema` is the idiomatic way to resolve the schema.
        This property exists only for symmetry with the DataFrame class.

        See Also
        --------
        collect_schema
        Schema

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.schema  # doctest: +SKIP
        Schema({'foo': Int64, 'bar': Float64, 'ham': String})
        """
        issue_warning(
            "Resolving the schema of a LazyFrame is a potentially expensive operation."
            " Use `LazyFrame.collect_schema()` to get the schema without this warning.",
            category=PerformanceWarning,
        )
        return self.collect_schema()
