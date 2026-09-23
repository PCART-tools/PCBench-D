def all(*names: str, ignore_nulls: bool = True) -> Expr:
    """
    Either return an expression representing all columns, or evaluate a bitwise AND operation.

    If no arguments are passed, this function is syntactic sugar for `col("*")`.
    Otherwise, this function is syntactic sugar for `col(names).all()`.

    Parameters
    ----------
    *names
        Name(s) of the columns to use in the aggregation.
    ignore_nulls
        Ignore null values (default).

        If set to `False`, `Kleene logic`_ is used to deal with nulls:
        if the column contains any null values and no `False` values,
        the output is null.

        .. _Kleene logic: https://en.wikipedia.org/wiki/Three-valued_logic

    See Also
    --------
    all_horizontal

    Examples
    --------
    Selecting all columns.

    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [True, False, True],
    ...         "b": [False, False, False],
    ...     }
    ... )
    >>> df.select(pl.all().sum())
    shape: (1, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ u32 ┆ u32 │
    ╞═════╪═════╡
    │ 2   ┆ 0   │
    └─────┴─────┘

    Evaluate bitwise AND for a column.

    >>> df.select(pl.all("a"))
    shape: (1, 1)
    ┌───────┐
    │ a     │
    │ ---   │
    │ bool  │
    ╞═══════╡
    │ false │
    └───────┘
    """  # noqa: W505
    if not names:
        return F.col("*")

    return F.col(*names).all(ignore_nulls=ignore_nulls)
