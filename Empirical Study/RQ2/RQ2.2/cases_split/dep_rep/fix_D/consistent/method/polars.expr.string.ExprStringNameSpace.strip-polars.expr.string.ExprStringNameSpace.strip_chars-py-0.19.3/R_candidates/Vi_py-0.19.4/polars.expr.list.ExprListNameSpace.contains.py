    def contains(
        self, item: float | str | bool | int | date | datetime | time | Expr
    ) -> Expr:
        """
        Check if sublists contain the given item.

        Parameters
        ----------
        item
            Item that will be checked for membership

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [[3, 2, 1], [], [1, 2]]})
        >>> df.select(pl.col("foo").list.contains(1))
        shape: (3, 1)
        ┌───────┐
        │ foo   │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ true  │
        │ false │
        │ true  │
        └───────┘

        """
        item = parse_as_expression(item, str_as_lit=True)
        return wrap_expr(self._pyexpr.list_contains(item))
