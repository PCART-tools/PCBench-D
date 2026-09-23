def any_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Compute the bitwise OR horizontally across columns.

    Parameters
    ----------
    *exprs
        Column(s) to use in the aggregation. Accepts expression input. Strings are
        parsed as column names, other non-expression inputs are parsed as literals.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [False, False, True, None],
    ...         "b": [False, True, None, None],
    ...         "c": ["w", "x", "y", "z"],
    ...     }
    ... )
    >>> df.with_columns(pl.any_horizontal("a", "b"))
    shape: (4, 4)
    ┌───────┬───────┬─────┬───────┐
    │ a     ┆ b     ┆ c   ┆ any   │
    │ ---   ┆ ---   ┆ --- ┆ ---   │
    │ bool  ┆ bool  ┆ str ┆ bool  │
    ╞═══════╪═══════╪═════╪═══════╡
    │ false ┆ false ┆ w   ┆ false │
    │ false ┆ true  ┆ x   ┆ true  │
    │ true  ┆ null  ┆ y   ┆ true  │
    │ null  ┆ null  ┆ z   ┆ null  │
    └───────┴───────┴─────┴───────┘

    """
    pyexprs = parse_as_list_of_expressions(*exprs)
    return wrap_expr(plr.any_horizontal(pyexprs))
