def first(*columns: str) -> Expr:
    """
    Get the first column or value.

    This function has different behavior depending on the presence of `columns`
    values. If none given (the default), returns an expression that takes the first
    column of the context; otherwise, takes the first value of the given column(s).

    Parameters
    ----------
    *columns
        One or more column names.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "baz"],
    ...     }
    ... )

    Return the first column:

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

    Return the first value for the given column(s):

    >>> df.select(pl.first("b"))
    shape: (1, 1)
    ┌─────┐
    │ b   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 4   │
    └─────┘
    >>> df.select(pl.first("a", "c"))
    shape: (1, 2)
    ┌─────┬─────┐
    │ a   ┆ c   │
    │ --- ┆ --- │
    │ i64 ┆ str │
    ╞═════╪═════╡
    │ 1   ┆ foo │
    └─────┴─────┘

    """
    if not columns:
        return wrap_expr(plr.first())

    return F.col(*columns).first()
