    def max(self) -> DataFrame:
        """
        Reduce the groups to the maximal value.

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
        >>> df.group_by("d", maintain_order=True).max()
        shape: (3, 4)
        ┌────────┬─────┬──────┬──────┐
        │ d      ┆ a   ┆ b    ┆ c    │
        │ ---    ┆ --- ┆ ---  ┆ ---  │
        │ str    ┆ i64 ┆ f64  ┆ bool │
        ╞════════╪═════╪══════╪══════╡
        │ Apple  ┆ 3   ┆ 10.0 ┆ true │
        │ Orange ┆ 2   ┆ 0.5  ┆ true │
        │ Banana ┆ 5   ┆ 14.0 ┆ true │
        └────────┴─────┴──────┴──────┘

        """
        return self.agg(F.all().max())
