def last(*columns: str) -> Expr:
    """
    Get the last column or value.

    This function has different behavior depending on the presence of `columns`
    values. If none given (the default), returns an expression that takes the last
    column of the context; otherwise, takes the last value of the given column(s).

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

    Return the last column:

    >>> df.select(pl.last())
    shape: (3, 1)
    ┌─────┐
    │ c   │
    │ --- │
    │ str │
    ╞═════╡
    │ foo │
    │ bar │
    │ baz │
    └─────┘

    Return the last value for the given column(s):

    >>> df.select(pl.last("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 3   │
    └─────┘
    >>> df.select(pl.last("b", "c"))
    shape: (1, 2)
    ┌─────┬─────┐
    │ b   ┆ c   │
    │ --- ┆ --- │
    │ i64 ┆ str │
    ╞═════╪═════╡
    │ 2   ┆ baz │
    └─────┴─────┘

    """
    if not columns:
        return wrap_expr(plr.last())

    return F.col(*columns).last()
