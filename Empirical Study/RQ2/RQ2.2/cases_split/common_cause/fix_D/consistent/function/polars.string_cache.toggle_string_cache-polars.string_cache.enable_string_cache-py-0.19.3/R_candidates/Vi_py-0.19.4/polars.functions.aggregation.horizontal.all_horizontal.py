def all_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Compute the bitwise AND horizontally across columns.

    Parameters
    ----------
    *exprs
        Column(s) to use in the aggregation. Accepts expression input. Strings are
        parsed as column names, other non-expression inputs are parsed as literals.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [False, False, True, True],
    ...         "b": [False, True, None, True],
    ...         "c": ["w", "x", "y", "z"],
    ...     }
    ... )
    >>> df.with_columns(pl.all_horizontal("a", "b"))
    shape: (4, 4)
    ┌───────┬───────┬─────┬───────┐
    │ a     ┆ b     ┆ c   ┆ all   │
    │ ---   ┆ ---   ┆ --- ┆ ---   │
    │ bool  ┆ bool  ┆ str ┆ bool  │
    ╞═══════╪═══════╪═════╪═══════╡
    │ false ┆ false ┆ w   ┆ false │
    │ false ┆ true  ┆ x   ┆ false │
    │ true  ┆ null  ┆ y   ┆ null  │
    │ true  ┆ true  ┆ z   ┆ true  │
    └───────┴───────┴─────┴───────┘

    """
    pyexprs = parse_as_list_of_expressions(*exprs)
    return wrap_expr(plr.all_horizontal(pyexprs))
