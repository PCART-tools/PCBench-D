    def cum_prod(self, *, reverse: bool = False) -> Expr:
        """
        Get an array with the cumulative product computed at every element.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Notes
        -----
        Dtypes in {Int8, UInt8, Int16, UInt16} are cast to
        Int64 before summing to prevent overflow issues.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3, 4]})
        >>> df.with_columns(
        ...     pl.col("a").cum_prod().alias("cum_prod"),
        ...     pl.col("a").cum_prod(reverse=True).alias("cum_prod_reverse"),
        ... )
        shape: (4, 3)
        ┌─────┬──────────┬──────────────────┐
        │ a   ┆ cum_prod ┆ cum_prod_reverse │
        │ --- ┆ ---      ┆ ---              │
        │ i64 ┆ i64      ┆ i64              │
        ╞═════╪══════════╪══════════════════╡
        │ 1   ┆ 1        ┆ 24               │
        │ 2   ┆ 2        ┆ 24               │
        │ 3   ┆ 6        ┆ 12               │
        │ 4   ┆ 24       ┆ 4                │
        └─────┴──────────┴──────────────────┘
        """
        return self._from_pyexpr(self._pyexpr.cum_prod(reverse))
