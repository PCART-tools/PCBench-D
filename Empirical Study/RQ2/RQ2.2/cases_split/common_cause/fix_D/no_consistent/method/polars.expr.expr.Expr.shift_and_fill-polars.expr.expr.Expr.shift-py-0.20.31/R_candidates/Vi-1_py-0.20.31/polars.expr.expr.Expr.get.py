    def get(self, index: int | Expr) -> Self:
        """
        Return a single value by index.

        Parameters
        ----------
        index
            An expression that leads to a UInt32 index.

        Returns
        -------
        Expr
            Expression of the same data type.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "group": [
        ...             "one",
        ...             "one",
        ...             "one",
        ...             "two",
        ...             "two",
        ...             "two",
        ...         ],
        ...         "value": [1, 98, 2, 3, 99, 4],
        ...     }
        ... )
        >>> df.group_by("group", maintain_order=True).agg(pl.col("value").get(1))
        shape: (2, 2)
        ┌───────┬───────┐
        │ group ┆ value │
        │ ---   ┆ ---   │
        │ str   ┆ i64   │
        ╞═══════╪═══════╡
        │ one   ┆ 98    │
        │ two   ┆ 99    │
        └───────┴───────┘
        """
        index_lit = parse_as_expression(index)
        return self._from_pyexpr(self._pyexpr.get(index_lit))
