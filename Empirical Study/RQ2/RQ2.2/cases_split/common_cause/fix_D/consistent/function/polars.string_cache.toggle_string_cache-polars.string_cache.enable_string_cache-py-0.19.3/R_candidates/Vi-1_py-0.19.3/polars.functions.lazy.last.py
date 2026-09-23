def last(column: str | Series | None = None) -> Expr:
    """
    Get the last value.

    Depending on the input type this function does different things:

    - None -> expression to take last column of a context.
    - str -> syntactic sugar for `pl.col(..).last()`
    - Series -> Take last value in `Series`

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.last())
    shape: (3, 1)
    ┌─────┐
    │ c   │
    │ --- │
    │ str │
    ╞═════╡
    │ foo │
    │ bar │
    │ foo │
    └─────┘
    >>> df.select(pl.last("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 3   │
    └─────┘

    """
    if column is None:
        return wrap_expr(plr.last())

    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `last` is deprecated. Use `series[-1]` instead.",
            version="0.18.8",
        )
        if column.len() > 0:
            return column[-1]
        else:
            raise IndexError("the series is empty, so no last value can be returned")
    return F.col(column).last()
