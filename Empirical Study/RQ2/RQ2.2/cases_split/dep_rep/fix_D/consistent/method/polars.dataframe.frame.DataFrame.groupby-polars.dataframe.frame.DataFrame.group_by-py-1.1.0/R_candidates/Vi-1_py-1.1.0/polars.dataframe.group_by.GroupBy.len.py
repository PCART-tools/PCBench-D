    def len(self, name: str | None = None) -> DataFrame:
        """
        Return the number of rows in each group.

        Parameters
        ----------
        name
            Assign a name to the resulting column; if unset, defaults to "len".

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["Apple", "Apple", "Orange"], "b": [1, None, 2]})
        >>> df.group_by("a").len()  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌────────┬─────┐
        │ a      ┆ len │
        │ ---    ┆ --- │
        │ str    ┆ u32 │
        ╞════════╪═════╡
        │ Apple  ┆ 2   │
        │ Orange ┆ 1   │
        └────────┴─────┘
        >>> df.group_by("a").len(name="n")  # doctest: +IGNORE_RESULT
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
