    def is_last_distinct(self) -> Self:
        """
        Return a boolean mask indicating the last occurrence of each distinct value.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 1, 2, 3, 2]})
        >>> df.with_columns(pl.col("a").is_last_distinct().alias("last"))
        shape: (5, 2)
        ┌─────┬───────┐
        │ a   ┆ last  │
        │ --- ┆ ---   │
        │ i64 ┆ bool  │
        ╞═════╪═══════╡
        │ 1   ┆ false │
        │ 1   ┆ true  │
        │ 2   ┆ false │
        │ 3   ┆ true  │
        │ 2   ┆ true  │
        └─────┴───────┘
        """
        return self._from_pyexpr(self._pyexpr.is_last_distinct())
