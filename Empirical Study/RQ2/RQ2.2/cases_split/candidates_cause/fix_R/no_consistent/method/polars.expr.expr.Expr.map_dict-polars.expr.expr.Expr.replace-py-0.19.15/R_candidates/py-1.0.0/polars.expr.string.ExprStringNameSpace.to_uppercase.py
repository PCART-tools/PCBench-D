    def to_uppercase(self) -> Expr:
        """
        Transform to uppercase variant.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["cat", "dog"]})
        >>> df.with_columns(foo_upper=pl.col("foo").str.to_uppercase())
        shape: (2, 2)
        ┌─────┬───────────┐
        │ foo ┆ foo_upper │
        │ --- ┆ ---       │
        │ str ┆ str       │
        ╞═════╪═══════════╡
        │ cat ┆ CAT       │
        │ dog ┆ DOG       │
        └─────┴───────────┘
        """
        return wrap_expr(self._pyexpr.str_to_uppercase())
