def any_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Compute the bitwise OR horizontally across columns.

    Parameters
    ----------
    *exprs
        Column(s) to use in the aggregation. Accepts expression input. Strings are
        parsed as column names, other non-expression inputs are parsed as literals.

    Notes
    -----
    `Kleene logic`_ is used to deal with nulls: if the column contains any null values
    and no `True` values, the output is null.

    .. _Kleene logic: https://en.wikipedia.org/wiki/Three-valued_logic

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [False, False, True, True, False, None],
    ...         "b": [False, True, True, None, None, None],
    ...         "c": ["u", "v", "w", "x", "y", "z"],
    ...     }
    ... )
    >>> df.with_columns(any=pl.any_horizontal("a", "b"))
    shape: (6, 4)
    ┌───────┬───────┬─────┬───────┐
    │ a     ┆ b     ┆ c   ┆ any   │
    │ ---   ┆ ---   ┆ --- ┆ ---   │
    │ bool  ┆ bool  ┆ str ┆ bool  │
    ╞═══════╪═══════╪═════╪═══════╡
    │ false ┆ false ┆ u   ┆ false │
    │ false ┆ true  ┆ v   ┆ true  │
    │ true  ┆ true  ┆ w   ┆ true  │
    │ true  ┆ null  ┆ x   ┆ true  │
    │ false ┆ null  ┆ y   ┆ null  │
    │ null  ┆ null  ┆ z   ┆ null  │
    └───────┴───────┴─────┴───────┘
    """
    pyexprs = parse_into_list_of_expressions(*exprs)
    return wrap_expr(plr.any_horizontal(pyexprs))
