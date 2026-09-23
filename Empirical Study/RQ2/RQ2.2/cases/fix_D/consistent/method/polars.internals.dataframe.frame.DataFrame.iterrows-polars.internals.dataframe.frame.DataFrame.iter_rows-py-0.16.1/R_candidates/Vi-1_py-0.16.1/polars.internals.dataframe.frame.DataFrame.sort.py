    def sort(
        self: DF,
        by: str | pli.Expr | Sequence[str] | Sequence[pli.Expr],
        *,
        reverse: bool | list[bool] = False,
        nulls_last: bool = False,
    ) -> DF | DataFrame:
        """
        Sort the DataFrame by column.

        Parameters
        ----------
        by
            By which column to sort. Only accepts string.
        reverse
            Reverse/descending sort.
        nulls_last
            Place null values last. Can only be used if sorted by a single column.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.sort("foo", reverse=True)
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ f64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 3   ┆ 8.0 ┆ c   │
        │ 2   ┆ 7.0 ┆ b   │
        │ 1   ┆ 6.0 ┆ a   │
        └─────┴─────┴─────┘

        **Sort by multiple columns.**
        For multiple columns we can also use expression syntax.

        >>> df.sort(
        ...     [pl.col("foo"), pl.col("bar") ** 2],
        ...     reverse=[True, False],
        ... )
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ f64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 3   ┆ 8.0 ┆ c   │
        │ 2   ┆ 7.0 ┆ b   │
        │ 1   ┆ 6.0 ┆ a   │
        └─────┴─────┴─────┘

        """
        if not isinstance(by, str) and isinstance(by, (Sequence, pli.Expr)):
            df = (
                self.lazy()
                .sort(by, reverse=reverse, nulls_last=nulls_last)
                .collect(no_optimization=True)
            )
            return df
        return self._from_pydf(self._df.sort(by, reverse, nulls_last))
