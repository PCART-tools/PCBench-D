    def head(self, n: int = 5) -> DataFrame:
        """
        Get the first `n` rows of each group.

        Parameters
        ----------
        n
            Number of rows to return.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "letters": ["c", "c", "a", "c", "a", "b"],
        ...         "nrs": [1, 2, 3, 4, 5, 6],
        ...     }
        ... )
        >>> df
        shape: (6, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ c       ┆ 1   │
        │ c       ┆ 2   │
        │ a       ┆ 3   │
        │ c       ┆ 4   │
        │ a       ┆ 5   │
        │ b       ┆ 6   │
        └─────────┴─────┘
        >>> df.group_by("letters").head(2).sort("letters")
        shape: (5, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ a       ┆ 3   │
        │ a       ┆ 5   │
        │ b       ┆ 6   │
        │ c       ┆ 1   │
        │ c       ┆ 2   │
        └─────────┴─────┘

        """
        return (
            self.df.lazy()
            .group_by(self.by, *self.more_by, maintain_order=self.maintain_order)
            .head(n)
            .collect(no_optimization=True)
        )
