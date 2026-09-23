def head(column: str | Series, n: int = 10) -> Expr | Series:
    """
    Get the first `n` rows.

    Parameters
    ----------
    column
        Column name or Series.
    n
        Number of rows to return.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.head("a"))
    shape: (3, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 8   │
    │ 3   │
    └─────┘
    >>> df.select(pl.head("a", 2))
    shape: (2, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 8   │
    └─────┘

    """
    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `head` is deprecated. Use `Series.head()` instead.",
            version="0.18.8",
        )
        return column.head(n)
    return F.col(column).head(n)
