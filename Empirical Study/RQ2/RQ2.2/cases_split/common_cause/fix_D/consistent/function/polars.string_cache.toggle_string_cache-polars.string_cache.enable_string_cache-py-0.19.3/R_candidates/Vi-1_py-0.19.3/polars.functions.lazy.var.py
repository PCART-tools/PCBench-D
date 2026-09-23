def var(column: str | Series, ddof: int = 1) -> Expr | float | None:
    """
    Get the variance.

    Parameters
    ----------
    column
        Column to get the variance of.
    ddof
        “Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof,
        where N represents the number of elements.
        By default ddof is 1.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.var("a"))
    shape: (1, 1)
    ┌──────┐
    │ a    │
    │ ---  │
    │ f64  │
    ╞══════╡
    │ 13.0 │
    └──────┘
    >>> df["a"].var()
    13.0

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `var` is deprecated. Use `Series.var()` instead.",
            version="0.18.8",
        )
        return column.var(ddof)
    return F.col(column).var(ddof)
