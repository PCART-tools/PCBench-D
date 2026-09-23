    @property
    def dtypes(self) -> list[DataType]:
        """
        Get the column data types.

        Returns
        -------
        list of DataType
            A list containing the data type of each column in order.

        Warnings
        --------
        Determining the data types of a LazyFrame requires resolving its schema,
        which is a potentially expensive operation.
        Using :meth:`collect_schema` is the idiomatic way to resolve the schema.
        This property exists only for symmetry with the DataFrame class.

        See Also
        --------
        collect_schema
        Schema.dtypes

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.dtypes  # doctest: +SKIP
        [Int64, Float64, String]
        """
        issue_warning(
            "Determining the data types of a LazyFrame requires resolving its schema,"
            " which is a potentially expensive operation. Use `LazyFrame.collect_schema().dtypes()`"
            " to get the data types without this warning.",
            category=PerformanceWarning,
        )
        return self.collect_schema().dtypes()
