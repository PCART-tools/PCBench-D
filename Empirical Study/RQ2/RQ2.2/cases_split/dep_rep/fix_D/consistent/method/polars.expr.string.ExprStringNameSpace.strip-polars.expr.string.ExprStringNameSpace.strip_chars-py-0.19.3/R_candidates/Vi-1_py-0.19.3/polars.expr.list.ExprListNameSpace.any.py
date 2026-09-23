    def any(self) -> Expr:
        """
        Evaluate whether any boolean value in a list is true.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[True, True], [False, True], [False, False], [None], [], None]}
        ... )
        >>> df.select(pl.col("a").list.any())
        shape: (6, 1)
        ┌───────┐
        │ a     │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ true  │
        │ true  │
        │ false │
        │ false │
        │ false │
        │ null  │
        └───────┘

        """
        return wrap_expr(self._pyexpr.list_any())
