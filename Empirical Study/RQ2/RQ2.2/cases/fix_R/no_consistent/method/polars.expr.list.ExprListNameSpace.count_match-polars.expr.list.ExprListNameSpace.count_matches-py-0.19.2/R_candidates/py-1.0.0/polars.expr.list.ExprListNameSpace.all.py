    def all(self) -> Expr:
        """
        Evaluate whether all boolean values in a list are true.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[True, True], [False, True], [False, False], [None], [], None]}
        ... )
        >>> df.with_columns(all=pl.col("a").list.all())
        shape: (6, 2)
        ┌────────────────┬───────┐
        │ a              ┆ all   │
        │ ---            ┆ ---   │
        │ list[bool]     ┆ bool  │
        ╞════════════════╪═══════╡
        │ [true, true]   ┆ true  │
        │ [false, true]  ┆ false │
        │ [false, false] ┆ false │
        │ [null]         ┆ true  │
        │ []             ┆ true  │
        │ null           ┆ null  │
        └────────────────┴───────┘
        """
        return wrap_expr(self._pyexpr.list_all())
