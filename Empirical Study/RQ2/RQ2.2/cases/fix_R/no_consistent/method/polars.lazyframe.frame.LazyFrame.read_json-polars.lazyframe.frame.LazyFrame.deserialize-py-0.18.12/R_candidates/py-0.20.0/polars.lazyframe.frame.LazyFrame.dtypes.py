    @property
    def dtypes(self) -> list[DataType]:
        """
        Get dtypes of columns in LazyFrame.

        See Also
        --------
        schema : Returns a {colname:dtype} mapping.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.dtypes
        [Int64, Float64, Utf8]

        """
        return self._ldf.dtypes()
