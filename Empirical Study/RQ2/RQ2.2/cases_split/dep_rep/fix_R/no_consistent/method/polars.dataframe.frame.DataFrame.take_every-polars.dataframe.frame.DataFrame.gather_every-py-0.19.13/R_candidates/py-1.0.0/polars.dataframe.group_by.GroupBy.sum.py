    def sum(self) -> DataFrame:
        """
        Reduce the groups to the sum.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 2, 3, 4, 5],
        ...         "b": [0.5, 0.5, 4, 10, 13, 14],
        ...         "c": [True, True, True, False, False, True],
        ...         "d": ["Apple", "Orange", "Apple", "Apple", "Banana", "Banana"],
        ...     }
        ... )
        >>> df.group_by("d", maintain_order=True).sum()
        shape: (3, 4)
        ┌────────┬─────┬──────┬─────┐
        │ d      ┆ a   ┆ b    ┆ c   │
        │ ---    ┆ --- ┆ ---  ┆ --- │
        │ str    ┆ i64 ┆ f64  ┆ u32 │
        ╞════════╪═════╪══════╪═════╡
        │ Apple  ┆ 6   ┆ 14.5 ┆ 2   │
        │ Orange ┆ 2   ┆ 0.5  ┆ 1   │
        │ Banana ┆ 9   ┆ 27.0 ┆ 1   │
        └────────┴─────┴──────┴─────┘
        """
        return self.agg(F.all().sum())
