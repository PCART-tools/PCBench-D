    def all(self) -> Expr:
        """
        Evaluate whether all boolean values in a list are true.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[True, True], [False, True], [False, False], [None], [], None]}
        ... )
        >>> df.select(pl.col("a").list.all())
        shape: (6, 1)
        ┌───────┐
        │ a     │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ true  │
        │ false │
        │ false │
        │ true  │
        │ true  │
        │ null  │
        └───────┘

        """
        return wrap_expr(self._pyexpr.list_all())
