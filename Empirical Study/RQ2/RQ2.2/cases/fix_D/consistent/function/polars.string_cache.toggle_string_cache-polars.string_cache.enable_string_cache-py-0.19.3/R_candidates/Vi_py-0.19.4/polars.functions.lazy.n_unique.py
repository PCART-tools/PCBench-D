def n_unique(column: str | Series) -> Expr | int:
    """
    Count unique values.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 1], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.n_unique("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 2   │
    └─────┘

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `n_unique` is deprecated. Use `Series.n_unique()` instead.",
            version="0.18.8",
        )
        return column.n_unique()
    return F.col(column).n_unique()
