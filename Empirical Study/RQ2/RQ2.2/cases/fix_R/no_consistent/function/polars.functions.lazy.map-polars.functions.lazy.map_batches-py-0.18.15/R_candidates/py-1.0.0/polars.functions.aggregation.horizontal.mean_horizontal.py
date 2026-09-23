def mean_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Compute the mean of all values horizontally across columns.

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
    >>> df.with_columns(mean=pl.mean_horizontal("a", "b"))
    shape: (3, 4)
    ┌─────┬──────┬─────┬──────┐
    │ a   ┆ b    ┆ c   ┆ mean │
    │ --- ┆ ---  ┆ --- ┆ ---  │
    │ i64 ┆ i64  ┆ str ┆ f64  │
    ╞═════╪══════╪═════╪══════╡
    │ 1   ┆ 4    ┆ x   ┆ 2.5  │
    │ 8   ┆ 5    ┆ y   ┆ 6.5  │
    │ 3   ┆ null ┆ z   ┆ 3.0  │
    └─────┴──────┴─────┴──────┘
    """
    pyexprs = parse_into_list_of_expressions(*exprs)
    return wrap_expr(plr.mean_horizontal(pyexprs))
