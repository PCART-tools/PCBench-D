    def last(self) -> Expr:
        """
        Get the last value of the sublists.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[3, 2, 1], [], [1, 2]]})
        >>> df.with_columns(last=pl.col("a").list.last())
        shape: (3, 2)
        ┌───────────┬──────┐
        │ a         ┆ last │
        │ ---       ┆ ---  │
        │ list[i64] ┆ i64  │
        ╞═══════════╪══════╡
        │ [3, 2, 1] ┆ 1    │
        │ []        ┆ null │
        │ [1, 2]    ┆ 2    │
        └───────────┴──────┘
        """
        return self.get(-1, null_on_oob=True)
