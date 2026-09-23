    @property
    def columns(self) -> list[str]:
        """
        Get the column names.

        Returns
        -------
        list of str
            A list containing the name of each column in order.

        Warnings
        --------
        Determining the column names of a LazyFrame requires resolving its schema,
        which is a potentially expensive operation.
        Using :meth:`collect_schema` is the idiomatic way of resolving the schema.
        This property exists only for symmetry with the DataFrame class.

        See Also
        --------
        collect_schema
        Schema.names

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... ).select("foo", "bar")
        >>> lf.columns  # doctest: +SKIP
        ['foo', 'bar']
        """
        issue_warning(
            "Determining the column names of a LazyFrame requires resolving its schema,"
            " which is a potentially expensive operation. Use `LazyFrame.collect_schema().names()`"
            " to get the column names without this warning.",
            category=PerformanceWarning,
        )
        return self.collect_schema().names()
