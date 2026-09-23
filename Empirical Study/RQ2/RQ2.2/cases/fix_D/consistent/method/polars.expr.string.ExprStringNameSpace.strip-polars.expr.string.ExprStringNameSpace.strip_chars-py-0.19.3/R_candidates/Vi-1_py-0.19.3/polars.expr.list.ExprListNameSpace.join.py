    def join(self, separator: str) -> Expr:
        """
        Join all string items in a sublist and place a separator between them.

        This errors if inner type of list `!= Utf8`.

        Parameters
        ----------
        separator
            string to separate the items with

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`.

        Examples
        --------
        >>> df = pl.DataFrame({"s": [["a", "b", "c"], ["x", "y"]]})
        >>> df.select(pl.col("s").list.join(" "))
        shape: (2, 1)
        ┌───────┐
        │ s     │
        │ ---   │
        │ str   │
        ╞═══════╡
        │ a b c │
        │ x y   │
        └───────┘

        """
        return wrap_expr(self._pyexpr.list_join(separator))
