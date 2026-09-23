def mean(*columns: str) -> Expr:
    """
    Get the mean value.

    This function is syntactic sugar for `pl.col(columns).mean()`.

    Parameters
    ----------
    *columns
        One or more column names.

    See Also
    --------
    mean_horizontal

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.mean("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 4.0 │
    └─────┘
    >>> df.select(pl.mean("a", "b"))
    shape: (1, 2)
    ┌─────┬──────────┐
    │ a   ┆ b        │
    │ --- ┆ ---      │
    │ f64 ┆ f64      │
    ╞═════╪══════════╡
    │ 4.0 ┆ 3.666667 │
    └─────┴──────────┘

    """
    return F.col(*columns).mean()
