    def count(self) -> LazyFrame:
        """
        Return the number of rows in each group.

        Rows containing null values count towards the total.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["apple", "apple", "orange"],
        ...         "b": [1, None, 2],
        ...     }
        ... )
        >>> lf.group_by("a").count().collect()  # doctest: +SKIP
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
