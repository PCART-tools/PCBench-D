    def __iter__(self) -> Self:
        """
        Allows iteration over the groups of the group by operation.

        Each group is represented by a tuple of `(name, data)`. The group names are
        tuples of the distinct group values that identify each group. If a single string
        was passed to `by`, the keys are a single value instead of a tuple.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["a", "a", "b"], "bar": [1, 2, 3]})
        >>> for name, data in df.group_by(["foo"]):  # doctest: +SKIP
        ...     print(name)
        ...     print(data)
        (a,)
        shape: (2, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 1   │
        │ a   ┆ 2   │
        └─────┴─────┘
        (b,)
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
            self.df.lazy()
            .group_by(*self.by, **self.named_by, maintain_order=self.maintain_order)
            .agg(F.first().agg_groups().alias(temp_col))
            .collect(no_optimization=True)
        ).rechunk()

        self._group_names = groups_df.select(F.all().exclude(temp_col)).iter_rows()
        self._group_indices = groups_df.select(temp_col).to_series()
        self._current_index = 0

        return self
