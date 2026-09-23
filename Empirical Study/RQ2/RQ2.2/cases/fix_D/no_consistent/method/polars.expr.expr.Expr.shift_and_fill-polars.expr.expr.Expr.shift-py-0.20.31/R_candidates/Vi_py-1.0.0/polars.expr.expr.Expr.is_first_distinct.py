    def is_first_distinct(self) -> Expr:
        """
        Return a boolean mask indicating the first occurrence of each distinct value.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 1, 2, 3, 2]})
        >>> df.with_columns(pl.col("a").is_first_distinct().alias("first"))
        shape: (5, 2)
        ┌─────┬───────┐
        │ a   ┆ first │
        │ --- ┆ ---   │
        │ i64 ┆ bool  │
        ╞═════╪═══════╡
        │ 1   ┆ true  │
        │ 1   ┆ false │
        │ 2   ┆ true  │
        │ 3   ┆ true  │
        │ 2   ┆ false │
        └─────┴───────┘
        """
        return self._from_pyexpr(self._pyexpr.is_first_distinct())
