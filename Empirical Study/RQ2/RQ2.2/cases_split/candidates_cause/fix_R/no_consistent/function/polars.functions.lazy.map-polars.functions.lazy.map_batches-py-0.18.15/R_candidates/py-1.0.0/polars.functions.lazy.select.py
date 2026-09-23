def select(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> DataFrame:
    """
    Run polars expressions without a context.

    This is syntactic sugar for running `df.select` on an empty DataFrame.

    Parameters
    ----------
    *exprs
        Column(s) to select, specified as positional arguments.
        Accepts expression input. Strings are parsed as column names,
        other non-expression inputs are parsed as literals.
    **named_exprs
        Additional columns to select, specified as keyword arguments.
        The columns will be renamed to the keyword used.

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> foo = pl.Series("foo", [1, 2, 3])
    >>> bar = pl.Series("bar", [3, 2, 1])
    >>> pl.select(min=pl.min_horizontal(foo, bar))
    shape: (3, 1)
    ┌─────┐
    │ min │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 2   │
    │ 1   │
    └─────┘
    """
    return pl.DataFrame().select(*exprs, **named_exprs)
