    @deprecate_renamed_function("len", version="0.20.5")
    def count(self) -> LazyFrame:
        """
        Return the number of rows in each group.

        .. deprecated:: 0.20.5
            This method has been renamed to :func:`LazyGroupBy.len`.

        Rows containing null values count towards the total.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["Apple", "Apple", "Orange"],
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
        │ Apple  ┆ 2     │
        │ Orange ┆ 1     │
        └────────┴───────┘
        """
        return self.agg(F.len().alias("count"))
