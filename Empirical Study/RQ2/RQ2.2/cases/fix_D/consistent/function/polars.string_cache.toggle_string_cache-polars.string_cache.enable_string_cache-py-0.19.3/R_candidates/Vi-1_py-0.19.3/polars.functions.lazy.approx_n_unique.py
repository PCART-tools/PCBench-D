def approx_n_unique(column: str | Expr) -> Expr:
    """
    Approximate count of unique values.

    This is done using the HyperLogLog++ algorithm for cardinality estimation.

    Parameters
    ----------
    column
        Column name or Series.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 1], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.approx_n_unique("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 2   │
    └─────┘

    """
    if isinstance(column, pl.Expr):
        return column.approx_n_unique()
    return F.col(column).approx_n_unique()
