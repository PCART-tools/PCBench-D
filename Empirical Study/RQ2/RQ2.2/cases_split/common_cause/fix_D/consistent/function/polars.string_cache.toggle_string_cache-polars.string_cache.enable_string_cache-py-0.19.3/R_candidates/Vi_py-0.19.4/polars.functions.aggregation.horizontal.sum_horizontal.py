def sum_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Sum all values horizontally across columns.

    Parameters
    ----------
    *exprs
        Column(s) to use in the aggregation. Accepts expression input. Strings are
        parsed as column names, other non-expression inputs are parsed as literals.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, None],
    ...         "c": ["x", "y", "z"],
    ...     }
    ... )
    >>> df.with_columns(pl.sum_horizontal("a", "b"))
    shape: (3, 4)
    ┌─────┬──────┬─────┬──────┐
    │ a   ┆ b    ┆ c   ┆ sum  │
    │ --- ┆ ---  ┆ --- ┆ ---  │
    │ i64 ┆ i64  ┆ str ┆ i64  │
    ╞═════╪══════╪═════╪══════╡
    │ 1   ┆ 4    ┆ x   ┆ 5    │
    │ 8   ┆ 5    ┆ y   ┆ 13   │
    │ 3   ┆ null ┆ z   ┆ null │
    └─────┴──────┴─────┴──────┘

    """
    pyexprs = parse_as_list_of_expressions(*exprs)
    return wrap_expr(plr.sum_horizontal(pyexprs))
