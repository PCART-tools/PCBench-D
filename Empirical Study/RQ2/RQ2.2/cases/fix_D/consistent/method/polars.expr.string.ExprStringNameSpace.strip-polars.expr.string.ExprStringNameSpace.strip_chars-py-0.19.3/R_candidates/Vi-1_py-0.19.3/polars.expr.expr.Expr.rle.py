    def rle(self) -> Self:
        """
        Get the lengths of runs of identical values.

        Returns
        -------
        Expr
            Expression of data type :class:`Struct` with Fields "lengths" and "values".

        Examples
        --------
        >>> df = pl.DataFrame(pl.Series("s", [1, 1, 2, 1, None, 1, 3, 3]))
        >>> df.select(pl.col("s").rle()).unnest("s")
        shape: (6, 2)
        ┌─────────┬────────┐
        │ lengths ┆ values │
        │ ---     ┆ ---    │
        │ i32     ┆ i64    │
        ╞═════════╪════════╡
        │ 2       ┆ 1      │
        │ 1       ┆ 2      │
        │ 1       ┆ 1      │
        │ 1       ┆ null   │
        │ 1       ┆ 1      │
        │ 2       ┆ 3      │
        └─────────┴────────┘
        """
        return self._from_pyexpr(self._pyexpr.rle())
