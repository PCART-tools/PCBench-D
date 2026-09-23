    def __iter__(self) -> GroupBy[DF]:
        """
        Allows iteration over the groups of the groupby operation.

        Returns
        -------
        Iterator returning tuples of (name, data) for each group.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["a", "a", "b"], "bar": [1, 2, 3]})
        >>> for name, data in df.groupby("foo"):  # doctest: +SKIP
        ...     print(name)
        ...     print(data)
        ...
        a
        shape: (2, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 1   │
        │ a   ┆ 2   │
        └─────┴─────┘
        b
        shape: (1, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ b   ┆ 3   │
        └─────┴─────┘

        """
        temp_col = "__POLARS_GB_GROUP_INDICES"
        groups_df = (
            pli.wrap_df(self._df)
            .lazy()
            .with_row_count(name=temp_col)
            .groupby(self.by, maintain_order=self.maintain_order)
            .agg(pli.col(temp_col))
            .collect(no_optimization=True)
        )

        group_names = groups_df.select(pli.all().exclude(temp_col))

        # When grouping by a single column, group name is a single value
        # When grouping by multiple columns, group name is a tuple of values
        self._group_names: Iterator[object] | Iterator[tuple[object, ...]]
        if isinstance(self.by, (str, pli.Expr)):
            self._group_names = iter(group_names.to_series())
        else:
            self._group_names = group_names.iter_rows()

        self._group_indices = groups_df.select(temp_col).to_series()
        self._current_index = 0

        return self
