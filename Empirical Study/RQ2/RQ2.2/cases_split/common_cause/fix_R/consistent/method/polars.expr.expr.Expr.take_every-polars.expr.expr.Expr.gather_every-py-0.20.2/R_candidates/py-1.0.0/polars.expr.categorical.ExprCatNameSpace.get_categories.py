    def get_categories(self) -> Expr:
        """
        Get the categories stored in this data type.

        Examples
        --------
        >>> df = pl.Series(
        ...     "cats", ["foo", "bar", "foo", "foo", "ham"], dtype=pl.Categorical
        ... ).to_frame()
        >>> df.select(pl.col("cats").cat.get_categories())
        shape: (3, 1)
        ┌──────┐
        │ cats │
        │ ---  │
        │ str  │
        ╞══════╡
        │ foo  │
        │ bar  │
        │ ham  │
        └──────┘
        """
        return wrap_expr(self._pyexpr.cat_get_categories())
