def median(column: str | Series) -> Expr | float | int | None:
    """
    Get the median value.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.median("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 3.0 │
    └─────┘

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `median` is deprecated. Use `Series.median()` instead.",
            version="0.18.8",
        )
        return column.median()
    return F.col(column).median()
