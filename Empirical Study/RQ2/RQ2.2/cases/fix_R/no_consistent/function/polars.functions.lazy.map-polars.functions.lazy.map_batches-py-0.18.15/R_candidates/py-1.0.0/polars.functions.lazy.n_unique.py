def n_unique(*columns: str) -> Expr:
    """
    Count unique values.

    This function is syntactic sugar for `pl.col(columns).n_unique()`.

    Parameters
    ----------
    columns
        One or more column names.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 1],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.n_unique("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 2   │
    └─────┘
    >>> df.select(pl.n_unique("b", "c"))
    shape: (1, 2)
    ┌─────┬─────┐
    │ b   ┆ c   │
    │ --- ┆ --- │
    │ u32 ┆ u32 │
    ╞═════╪═════╡
    │ 3   ┆ 2   │
    └─────┴─────┘

    """
    return F.col(*columns).n_unique()
