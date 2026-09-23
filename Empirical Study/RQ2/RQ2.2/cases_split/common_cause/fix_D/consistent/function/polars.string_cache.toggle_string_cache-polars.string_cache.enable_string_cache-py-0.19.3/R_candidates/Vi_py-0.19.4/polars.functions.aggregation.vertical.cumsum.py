def cumsum(*names: str) -> Expr:
    """
    Cumulatively sum all values.

    Syntactic sugar for ``col(names).cumsum()``.

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
    >>> df.select(pl.cumsum("a"))
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
    return F.col(*names).cumsum()
