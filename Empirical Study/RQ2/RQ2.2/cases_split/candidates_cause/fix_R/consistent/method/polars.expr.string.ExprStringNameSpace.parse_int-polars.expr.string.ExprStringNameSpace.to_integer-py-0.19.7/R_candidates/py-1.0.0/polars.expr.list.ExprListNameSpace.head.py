    def head(self, n: int | str | Expr = 5) -> Expr:
        """
        Slice the first `n` values of every sublist.

        Parameters
        ----------
        n
            Number of values to return for each sublist.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[1, 2, 3, 4], [10, 2, 1]]})
        >>> df.with_columns(head=pl.col("a").list.head(2))
        shape: (2, 2)
        ┌─────────────┬───────────┐
        │ a           ┆ head      │
        │ ---         ┆ ---       │
        │ list[i64]   ┆ list[i64] │
        ╞═════════════╪═══════════╡
        │ [1, 2, … 4] ┆ [1, 2]    │
        │ [10, 2, 1]  ┆ [10, 2]   │
        └─────────────┴───────────┘
        """
        return self.slice(0, n)
