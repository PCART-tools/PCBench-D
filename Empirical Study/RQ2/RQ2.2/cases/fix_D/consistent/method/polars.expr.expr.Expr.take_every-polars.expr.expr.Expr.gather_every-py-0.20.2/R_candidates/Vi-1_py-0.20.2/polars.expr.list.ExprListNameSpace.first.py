    def first(self) -> Expr:
        """
        Get the first value of the sublists.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[3, 2, 1], [], [1, 2]]})
        >>> df.with_columns(first=pl.col("a").list.first())
        shape: (3, 2)
        ┌───────────┬───────┐
        │ a         ┆ first │
        │ ---       ┆ ---   │
        │ list[i64] ┆ i64   │
        ╞═══════════╪═══════╡
        │ [3, 2, 1] ┆ 3     │
        │ []        ┆ null  │
        │ [1, 2]    ┆ 1     │
        └───────────┴───────┘

        """
        return self.get(0)
