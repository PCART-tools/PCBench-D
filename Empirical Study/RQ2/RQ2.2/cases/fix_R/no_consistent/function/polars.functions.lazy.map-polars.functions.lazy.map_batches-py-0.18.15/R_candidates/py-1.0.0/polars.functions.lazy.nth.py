def nth(*indices: int | Sequence[int]) -> Expr:
    """
    Get the nth column(s) of the context.

    Parameters
    ----------
    indices
        One or more indices representing the columns to retrieve.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "baz"],
    ...     }
    ... )
    >>> df.select(pl.nth(1))
    shape: (3, 1)
    ┌─────┐
    │ b   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 4   │
    │ 5   │
    │ 2   │
    └─────┘
    >>> df.select(pl.nth(2, 0))
    shape: (3, 2)
    ┌─────┬─────┐
    │ c   ┆ a   │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ foo ┆ 1   │
    │ bar ┆ 8   │
    │ baz ┆ 3   │
    └─────┴─────┘
    """
    if len(indices) == 1 and isinstance(indices[0], Sequence):
        indices = indices[0]  # type: ignore[assignment]

    return wrap_expr(plr.index_cols(indices))
