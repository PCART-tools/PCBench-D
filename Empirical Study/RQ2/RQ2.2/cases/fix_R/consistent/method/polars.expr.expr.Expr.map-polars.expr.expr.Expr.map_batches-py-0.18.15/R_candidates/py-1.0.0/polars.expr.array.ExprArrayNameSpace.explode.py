    def explode(self) -> Expr:
        """
        Returns a column with a separate row for every array element.

        Returns
        -------
        Expr
            Expression with the data type of the array elements.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[1, 2, 3], [4, 5, 6]]}, schema={"a": pl.Array(pl.Int64, 3)}
        ... )
        >>> df.select(pl.col("a").arr.explode())
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
