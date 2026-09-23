    @deprecate_renamed_function("len", version="0.20.5")
    def count(self) -> DataFrame:
        """
        Return the number of rows in each group.

        .. deprecated:: 0.20.5
            This method has been renamed to :func:`GroupBy.len`.

        Rows containing null values count towards the total.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": ["Apple", "Apple", "Orange"],
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
        │ Apple  ┆ 2     │
        │ Orange ┆ 1     │
        └────────┴───────┘
        """
        return self.agg(F.len().alias("count"))
