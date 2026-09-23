    def count(self) -> DataFrame:
        """
        Return the number of rows in each group.

        Rows containing null values count towards the total.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": ["apple", "apple", "orange"],
        ...         "b": [1, None, 2],
        ...     }
        ... )
        >>> df.group_by("a").count()  # doctest: +SKIP
        shape: (2, 2)
        ┌────────┬───────┐
        │ a      ┆ count │
        │ ---    ┆ ---   │
        │ str    ┆ u32   │
        ╞════════╪═══════╡
        │ apple  ┆ 2     │
        │ orange ┆ 1     │
        └────────┴───────┘
        """
        return self.agg(F.count())
