def mean(column: str | Series) -> Expr | float | None:
    """
    Get the mean value.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.mean("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 4.0 │
    └─────┘

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `mean` is deprecated. Use `Series.mean()` instead.",
            version="0.18.8",
        )
        return column.mean()
    return F.col(column).mean()
