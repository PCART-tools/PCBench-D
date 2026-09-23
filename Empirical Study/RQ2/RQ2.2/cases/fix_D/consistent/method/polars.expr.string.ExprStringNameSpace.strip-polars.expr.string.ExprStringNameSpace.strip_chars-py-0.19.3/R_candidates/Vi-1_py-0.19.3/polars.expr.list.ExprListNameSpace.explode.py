    def explode(self) -> Expr:
        """
        Returns a column with a separate row for every list element.

        Returns
        -------
        Expr
            Expression with the data type of the list elements.

        See Also
        --------
        ExprNameSpace.reshape: Reshape this Expr to a flat Series or a Series of Lists.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[1, 2, 3], [4, 5, 6]]})
        >>> df.select(pl.col("a").list.explode())
        shape: (6, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 1   │
        │ 2   │
        │ 3   │
        │ 4   │
        │ 5   │
        │ 6   │
        └─────┘

        """
        return wrap_expr(self._pyexpr.explode())
