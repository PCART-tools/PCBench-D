    def to_lowercase(self) -> Expr:
        """
        Transform to lowercase variant.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["CAT", "DOG"]})
        >>> df.select(pl.col("foo").str.to_lowercase())
        shape: (2, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ str │
        ╞═════╡
        │ cat │
        │ dog │
        └─────┘

        """
        return wrap_expr(self._pyexpr.str_to_lowercase())
