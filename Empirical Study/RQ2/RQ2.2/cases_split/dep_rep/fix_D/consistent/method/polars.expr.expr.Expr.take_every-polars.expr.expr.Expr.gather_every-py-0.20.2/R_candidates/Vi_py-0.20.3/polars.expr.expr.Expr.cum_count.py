    def cum_count(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative count computed at every element.

        Counting from 0 to len

        Parameters
        ----------
        reverse
            Reverse the operation.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3, 4]})
        >>> df.with_columns(
        ...     pl.col("a").cum_count().alias("cum_count"),
        ...     pl.col("a").cum_count(reverse=True).alias("cum_count_reverse"),
        ... )
        shape: (4, 3)
        ┌─────┬───────────┬───────────────────┐
        │ a   ┆ cum_count ┆ cum_count_reverse │
        │ --- ┆ ---       ┆ ---               │
        │ i64 ┆ u32       ┆ u32               │
        ╞═════╪═══════════╪═══════════════════╡
        │ 1   ┆ 0         ┆ 3                 │
        │ 2   ┆ 1         ┆ 2                 │
        │ 3   ┆ 2         ┆ 1                 │
        │ 4   ┆ 3         ┆ 0                 │
        └─────┴───────────┴───────────────────┘

        """
        return self._from_pyexpr(self._pyexpr.cum_count(reverse))
