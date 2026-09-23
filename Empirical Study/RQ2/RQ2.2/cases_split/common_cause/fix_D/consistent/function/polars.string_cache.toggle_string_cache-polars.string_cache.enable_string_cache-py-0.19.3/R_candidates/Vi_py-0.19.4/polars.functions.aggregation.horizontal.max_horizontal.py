def max_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Get the maximum value horizontally across columns.

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
    >>> df.with_columns(pl.max_horizontal("a", "b"))
    shape: (3, 4)
    ┌─────┬──────┬─────┬─────┐
    │ a   ┆ b    ┆ c   ┆ max │
    │ --- ┆ ---  ┆ --- ┆ --- │
    │ i64 ┆ i64  ┆ str ┆ i64 │
    ╞═════╪══════╪═════╪═════╡
    │ 1   ┆ 4    ┆ x   ┆ 4   │
    │ 8   ┆ 5    ┆ y   ┆ 8   │
    │ 3   ┆ null ┆ z   ┆ 3   │
    └─────┴──────┴─────┴─────┘

    """
    pyexprs = parse_as_list_of_expressions(*exprs)
    return wrap_expr(plr.max_horizontal(pyexprs))
