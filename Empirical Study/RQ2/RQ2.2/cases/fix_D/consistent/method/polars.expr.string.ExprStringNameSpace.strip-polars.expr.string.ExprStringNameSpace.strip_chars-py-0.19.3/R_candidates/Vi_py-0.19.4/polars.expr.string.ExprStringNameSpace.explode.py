    def explode(self) -> Expr:
        """
        Returns a column with a separate row for every string character.

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["foo", "bar"]})
        >>> df.select(pl.col("a").str.explode())
        shape: (6, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ str │
        ╞═════╡
        │ f   │
        │ o   │
        │ o   │
        │ b   │
        │ a   │
        │ r   │
        └─────┘

        """
        return wrap_expr(self._pyexpr.str_explode())
