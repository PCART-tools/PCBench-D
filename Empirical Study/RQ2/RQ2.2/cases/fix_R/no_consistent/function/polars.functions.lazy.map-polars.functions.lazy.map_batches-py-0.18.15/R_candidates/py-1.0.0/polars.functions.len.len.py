def len() -> Expr:
    """
    Return the number of rows in the context.

    This is similar to `COUNT(*)` in SQL.

    Returns
    -------
    Expr
        Expression of data type :class:`UInt32`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 2, None],
    ...         "b": [3, None, None],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.len())
    shape: (1, 1)
    ┌─────┐
    │ len │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 3   │
    └─────┘

    Generate an index column by using `len` in conjunction with :func:`int_range`.

    >>> df.select(
    ...     pl.int_range(pl.len(), dtype=pl.UInt32).alias("index"),
    ...     pl.all(),
    ... )
    shape: (3, 4)
    ┌───────┬──────┬──────┬─────┐
    │ index ┆ a    ┆ b    ┆ c   │
    │ ---   ┆ ---  ┆ ---  ┆ --- │
    │ u32   ┆ i64  ┆ i64  ┆ str │
    ╞═══════╪══════╪══════╪═════╡
    │ 0     ┆ 1    ┆ 3    ┆ foo │
    │ 1     ┆ 2    ┆ null ┆ bar │
    │ 2     ┆ null ┆ null ┆ foo │
    └───────┴──────┴──────┴─────┘
    """
    return wrap_expr(plr.len())
