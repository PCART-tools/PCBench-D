def std(column: str | Series, ddof: int = 1) -> Expr | float | None:
    """
    Get the standard deviation.

    Parameters
    ----------
    column
        Column to get the standard deviation from.
    ddof
        “Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof,
        where N represents the number of elements.
        By default ddof is 1.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.std("a"))
    shape: (1, 1)
    ┌──────────┐
    │ a        │
    │ ---      │
    │ f64      │
    ╞══════════╡
    │ 3.605551 │
    └──────────┘
    >>> df["a"].std()
    3.605551275463989

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `std` is deprecated. Use `Series.std()` instead.",
            version="0.18.8",
        )
        return column.std(ddof)
    return F.col(column).std(ddof)
