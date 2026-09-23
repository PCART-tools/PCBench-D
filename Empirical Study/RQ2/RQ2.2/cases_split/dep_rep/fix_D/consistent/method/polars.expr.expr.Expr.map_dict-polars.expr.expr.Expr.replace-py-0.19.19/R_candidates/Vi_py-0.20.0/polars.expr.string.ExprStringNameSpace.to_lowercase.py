    def to_lowercase(self) -> Expr:
        """
        Transform to lowercase variant.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["CAT", "DOG"]})
        >>> df.with_columns(foo_lower=pl.col("foo").str.to_lowercase())
        shape: (2, 2)
        ┌─────┬───────────┐
        │ foo ┆ foo_lower │
        │ --- ┆ ---       │
        │ str ┆ str       │
        ╞═════╪═══════════╡
        │ CAT ┆ cat       │
        │ DOG ┆ dog       │
        └─────┴───────────┘

        """
        return wrap_expr(self._pyexpr.str_to_lowercase())
