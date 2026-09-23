    def any(self) -> Expr:
        """
        Evaluate whether any boolean value in a list is true.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[True, True], [False, True], [False, False], [None], [], None]}
        ... )
        >>> df.with_columns(any=pl.col("a").list.any())
        shape: (6, 2)
        ┌────────────────┬───────┐
        │ a              ┆ any   │
        │ ---            ┆ ---   │
        │ list[bool]     ┆ bool  │
        ╞════════════════╪═══════╡
        │ [true, true]   ┆ true  │
        │ [false, true]  ┆ true  │
        │ [false, false] ┆ false │
        │ [null]         ┆ false │
        │ []             ┆ false │
        │ null           ┆ null  │
        └────────────────┴───────┘
        """
        return wrap_expr(self._pyexpr.list_any())
