def implode(*columns: str) -> Expr:
    """
    Aggregate all column values into a list.

    This function is syntactic sugar for `pl.col(name).implode()`.

    Parameters
    ----------
    *columns
        One or more column names.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 2, 3],
    ...         "b": [9, 8, 7],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.implode("a"))
    shape: (1, 1)
    ┌───────────┐
    │ a         │
    │ ---       │
    │ list[i64] │
    ╞═══════════╡
    │ [1, 2, 3] │
    └───────────┘
    >>> df.select(pl.implode("b", "c"))
    shape: (1, 2)
    ┌───────────┬───────────────────────┐
    │ b         ┆ c                     │
    │ ---       ┆ ---                   │
    │ list[i64] ┆ list[str]             │
    ╞═══════════╪═══════════════════════╡
    │ [9, 8, 7] ┆ ["foo", "bar", "foo"] │
    └───────────┴───────────────────────┘

    """
    return F.col(*columns).implode()
