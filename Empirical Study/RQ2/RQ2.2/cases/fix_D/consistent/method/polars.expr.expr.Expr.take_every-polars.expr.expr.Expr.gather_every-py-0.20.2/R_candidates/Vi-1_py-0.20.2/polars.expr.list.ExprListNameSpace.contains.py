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
        >>> df = pl.DataFrame({"a": [[3, 2, 1], [], [1, 2]]})
        >>> df.with_columns(contains=pl.col("a").list.contains(1))
        shape: (3, 2)
        ┌───────────┬──────────┐
        │ a         ┆ contains │
        │ ---       ┆ ---      │
        │ list[i64] ┆ bool     │
        ╞═══════════╪══════════╡
        │ [3, 2, 1] ┆ true     │
        │ []        ┆ false    │
        │ [1, 2]    ┆ true     │
        └───────────┴──────────┘

        """
        item = parse_as_expression(item, str_as_lit=True)
        return wrap_expr(self._pyexpr.list_contains(item))
