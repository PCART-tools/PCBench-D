    def drop_nulls(self) -> Expr:
        """
        Drop all null values in the list.

        The original order of the remaining elements is preserved.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[None, 1, None, 2], [None], [3, 4]]})
        >>> df.select(pl.col("values").list.drop_nulls())
        shape: (3, 1)
        ┌───────────┐
        │ values    │
        │ ---       │
        │ list[i64] │
        ╞═══════════╡
        │ [1, 2]    │
        │ []        │
        │ [3, 4]    │
        └───────────┘

        """
        return wrap_expr(self._pyexpr.list_drop_nulls())
