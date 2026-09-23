def first(column: str | Series | None = None) -> Expr | Any:
    """
    Get the first value.

    Depending on the input type this function does different things:

    input:

    - None -> expression to take first column of a context.
    - str -> syntactic sugar for `pl.col(..).first()`
    - Series -> Take first value in `Series`

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.first())
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
    >>> df.select(pl.first("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    └─────┘

    """
    if column is None:
        return wrap_expr(plr.first())

    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `first` is deprecated. Use `series[0]` instead.",
            version="0.18.8",
        )
        if column.len() > 0:
            return column[0]
        else:
            raise IndexError("the series is empty, so no first value can be returned")
    return F.col(column).first()
