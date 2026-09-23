    def explode(self) -> Expr:
        """
        Explode a list expression.

        This means that every item is expanded to a new row.

        Returns
        -------
        Expr
            Expression with the data type of the list elements.

        See Also
        --------
        Expr.list.explode : Explode a list column.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "group": ["a", "b"],
        ...         "values": [
        ...             [1, 2],
        ...             [3, 4],
        ...         ],
        ...     }
        ... )
        >>> df.select(pl.col("values").explode())
        shape: (4, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ 1      │
        │ 2      │
        │ 3      │
        │ 4      │
        └────────┘
        """
        return self._from_pyexpr(self._pyexpr.explode())
