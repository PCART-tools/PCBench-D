    @property
    def width(self) -> int:
        """
        Get the number of columns.

        Returns
        -------
        int

        Warnings
        --------
        Determining the width of a LazyFrame requires resolving its schema,
        which is a potentially expensive operation.
        Using :meth:`collect_schema` is the idiomatic way to resolve the schema.
        This property exists only for symmetry with the DataFrame class.

        See Also
        --------
        collect_schema
        Schema.len

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4, 5, 6],
        ...     }
        ... )
        >>> lf.width  # doctest: +SKIP
        2
        """
        issue_warning(
            "Determining the width of a LazyFrame requires resolving its schema,"
            " which is a potentially expensive operation. Use `LazyFrame.collect_schema().len()`"
            " to get the width without this warning.",
            category=PerformanceWarning,
        )
        return self.collect_schema().len()
