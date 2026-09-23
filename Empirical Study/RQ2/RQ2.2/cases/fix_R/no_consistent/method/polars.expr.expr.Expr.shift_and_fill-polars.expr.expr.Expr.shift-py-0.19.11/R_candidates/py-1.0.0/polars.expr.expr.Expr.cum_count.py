    def cum_count(self, *, reverse: bool = False) -> Expr:
        """
        Return the cumulative count of the non-null values in the column.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["x", "k", None, "d"]})
        >>> df.with_columns(
        ...     pl.col("a").cum_count().alias("cum_count"),
        ...     pl.col("a").cum_count(reverse=True).alias("cum_count_reverse"),
        ... )
        shape: (4, 3)
        ┌──────┬───────────┬───────────────────┐
        │ a    ┆ cum_count ┆ cum_count_reverse │
        │ ---  ┆ ---       ┆ ---               │
        │ str  ┆ u32       ┆ u32               │
        ╞══════╪═══════════╪═══════════════════╡
        │ x    ┆ 1         ┆ 3                 │
        │ k    ┆ 2         ┆ 2                 │
        │ null ┆ 2         ┆ 1                 │
        │ d    ┆ 3         ┆ 1                 │
        └──────┴───────────┴───────────────────┘
        """
        return self._from_pyexpr(self._pyexpr.cum_count(reverse))
