    @deprecate_function(
        "DataFrame.replace is deprecated and will be removed in a future version. "
        "Please use\n"
        "    df = df.with_columns(new_column.alias(column_name))\n"
        "instead.",
        version="0.19.0",
    )
    def replace(self, column: str, new_column: Series) -> Self:
        """
        Replace a column by a new Series.

        Parameters
        ----------
        column
            Column to replace.
        new_column
            New column to insert.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> s = pl.Series([10, 20, 30])
        >>> df.replace("foo", s)  # works in-place!  # doctest: +SKIP
        shape: (3, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 10  ┆ 4   │
        │ 20  ┆ 5   │
        │ 30  ┆ 6   │
        └─────┴─────┘

        """
        return self._replace(column, new_column)
