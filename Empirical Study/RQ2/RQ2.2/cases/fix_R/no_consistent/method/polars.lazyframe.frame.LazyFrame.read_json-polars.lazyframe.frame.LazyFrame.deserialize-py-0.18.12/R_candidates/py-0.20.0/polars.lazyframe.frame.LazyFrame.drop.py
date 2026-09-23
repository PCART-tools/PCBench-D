    def drop(
        self,
        columns: ColumnNameOrSelector | Collection[ColumnNameOrSelector],
        *more_columns: ColumnNameOrSelector,
    ) -> Self:
        """
        Remove columns from the DataFrame.

        Parameters
        ----------
        columns
            Name of the column(s) that should be removed from the DataFrame.
        *more_columns
            Additional columns to drop, specified as positional arguments.

        Examples
        --------
        Drop a single column by passing the name of that column.

        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.drop("ham").collect()
        shape: (3, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ f64 │
        ╞═════╪═════╡
        │ 1   ┆ 6.0 │
        │ 2   ┆ 7.0 │
        │ 3   ┆ 8.0 │
        └─────┴─────┘

        Drop multiple columns by passing a selector.

        >>> import polars.selectors as cs
        >>> lf.drop(cs.numeric()).collect()
        shape: (3, 1)
        ┌─────┐
        │ ham │
        │ --- │
        │ str │
        ╞═════╡
        │ a   │
        │ b   │
        │ c   │
        └─────┘

        Use positional arguments to drop multiple columns.

        >>> lf.drop("foo", "ham").collect()
        shape: (3, 1)
        ┌─────┐
        │ bar │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 6.0 │
        │ 7.0 │
        │ 8.0 │
        └─────┘

        """
        drop_cols = _expand_selectors(self, columns, *more_columns)
        return self._from_pyldf(self._ldf.drop(drop_cols))
