def cum_sum(*names: str) -> Expr:
    """
    Cumulatively sum all values.

    Syntactic sugar for `col(names).cum_sum()`.

    Parameters
    ----------
    *names
        Name(s) of the columns to use in the aggregation.

    See Also
    --------
    cumsum_horizontal

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 2, 3],
    ...         "b": [4, 5, 6],
    ...     }
    ... )
    >>> df.select(pl.cum_sum("a"))
    shape: (3, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 3   │
    │ 6   │
    └─────┘
    """
    return F.col(*names).cum_sum()
