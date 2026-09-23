def all_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Compute the bitwise AND horizontally across columns.

    Parameters
    ----------
    *exprs
        Column(s) to use in the aggregation. Accepts expression input. Strings are
        parsed as column names, other non-expression inputs are parsed as literals.

    Notes
    -----
    `Kleene logic`_ is used to deal with nulls: if the column contains any null values
    and no `False` values, the output is null.

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
    >>> df.with_columns(all=pl.all_horizontal("a", "b"))
    shape: (6, 4)
    ┌───────┬───────┬─────┬───────┐
    │ a     ┆ b     ┆ c   ┆ all   │
    │ ---   ┆ ---   ┆ --- ┆ ---   │
    │ bool  ┆ bool  ┆ str ┆ bool  │
    ╞═══════╪═══════╪═════╪═══════╡
    │ false ┆ false ┆ u   ┆ false │
    │ false ┆ true  ┆ v   ┆ false │
    │ true  ┆ true  ┆ w   ┆ true  │
    │ true  ┆ null  ┆ x   ┆ null  │
    │ false ┆ null  ┆ y   ┆ false │
    │ null  ┆ null  ┆ z   ┆ null  │
    └───────┴───────┴─────┴───────┘
    """
    pyexprs = parse_into_list_of_expressions(*exprs)
    return wrap_expr(plr.all_horizontal(pyexprs))
