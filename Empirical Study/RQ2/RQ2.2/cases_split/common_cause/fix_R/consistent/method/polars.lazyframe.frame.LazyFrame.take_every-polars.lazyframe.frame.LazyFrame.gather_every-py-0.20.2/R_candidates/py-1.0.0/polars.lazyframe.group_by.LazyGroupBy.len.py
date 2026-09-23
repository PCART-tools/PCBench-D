    def len(self, name: str | None = None) -> LazyFrame:
        """
        Return the number of rows in each group.

        Parameters
        ----------
        name
            Assign a name to the resulting column; if unset, defaults to "len".

        Examples
        --------
        >>> lf = pl.LazyFrame({"a": ["Apple", "Apple", "Orange"], "b": [1, None, 2]})
        >>> lf.group_by("a").len().collect()  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌────────┬─────┐
        │ a      ┆ len │
        │ ---    ┆ --- │
        │ str    ┆ u32 │
        ╞════════╪═════╡
        │ Apple  ┆ 2   │
        │ Orange ┆ 1   │
        └────────┴─────┘
        >>> lf.group_by("a").len(name="n").collect()  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌────────┬─────┐
        │ a      ┆ n   │
        │ ---    ┆ --- │
        │ str    ┆ u32 │
        ╞════════╪═════╡
        │ Apple  ┆ 2   │
        │ Orange ┆ 1   │
        └────────┴─────┘
        """
        len_expr = F.len()
        if name is not None:
            len_expr = len_expr.alias(name)
        return self.agg(len_expr)
