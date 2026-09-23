    def unique(
        self: DF,
        maintain_order: bool = True,
        subset: str | Sequence[str] | None = None,
        keep: UniqueKeepStrategy = "first",
    ) -> DF:
        """
        Drop duplicate rows from this DataFrame.

        Parameters
        ----------
        maintain_order
            Keep the same order as the original DataFrame. This is more expensive to
            compute.
        subset
            Columns to consider for identifying duplicates. Defaults to using all
            columns.
        keep : {'first', 'last', 'none'}
            Which of the duplicate rows to keep.

        Returns
        -------
        DataFrame with unique rows.

        Warnings
        --------
        This method will fail if there is a column of type `List` in the DataFrame or
        subset.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 1],
        ...         "bar": ["a", "a", "a", "a"],
        ...         "ham": ["b", "b", "b", "b"],
        ...     }
        ... )
        >>> df.unique()
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ str ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ a   ┆ b   │
        │ 2   ┆ a   ┆ b   │
        │ 3   ┆ a   ┆ b   │
        └─────┴─────┴─────┘
        >>> df.unique(subset=["bar", "ham"])
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ str ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ a   ┆ b   │
        └─────┴─────┴─────┘
        >>> df.unique(keep="last")
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ str ┆ str │
        ╞═════╪═════╪═════╡
        │ 2   ┆ a   ┆ b   │
        │ 3   ┆ a   ┆ b   │
        │ 1   ┆ a   ┆ b   │
        └─────┴─────┴─────┘

        """
        if subset is not None:
            if isinstance(subset, str):
                subset = [subset]
            elif not isinstance(subset, list):
                subset = list(subset)

        return self._from_pydf(self._df.unique(maintain_order, subset, keep))
