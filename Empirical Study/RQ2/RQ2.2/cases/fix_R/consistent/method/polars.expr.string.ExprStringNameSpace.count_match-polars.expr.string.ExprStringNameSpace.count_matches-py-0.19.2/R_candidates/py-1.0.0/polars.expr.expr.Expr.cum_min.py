    def cum_min(self, *, reverse: bool = False) -> Expr:
        """
        Get an array with the cumulative min computed at every element.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [3, 1, 2]})
        >>> df.with_columns(
        ...     pl.col("a").cum_min().alias("cum_min"),
        ...     pl.col("a").cum_min(reverse=True).alias("cum_min_reverse"),
        ... )
        shape: (3, 3)
        ┌─────┬─────────┬─────────────────┐
        │ a   ┆ cum_min ┆ cum_min_reverse │
        │ --- ┆ ---     ┆ ---             │
        │ i64 ┆ i64     ┆ i64             │
        ╞═════╪═════════╪═════════════════╡
        │ 3   ┆ 3       ┆ 1               │
        │ 1   ┆ 1       ┆ 1               │
        │ 2   ┆ 1       ┆ 2               │
        └─────┴─────────┴─────────────────┘

        """
        return self._from_pyexpr(self._pyexpr.cum_min(reverse))
