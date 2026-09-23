    def drop(
        self,
        *columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector],
        strict: bool = True,
    ) -> LazyFrame:
        """
        Remove columns from the DataFrame.

        Parameters
        ----------
        *columns
            Names of the columns that should be removed from the dataframe.
            Accepts column selector input.
        strict
            Validate that all column names exist in the schema and throw an
            exception if a column name does not exist in the schema.

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
        drop_cols = _expand_selectors(self, *columns)
        return self._from_pyldf(self._ldf.drop(drop_cols, strict=strict))
