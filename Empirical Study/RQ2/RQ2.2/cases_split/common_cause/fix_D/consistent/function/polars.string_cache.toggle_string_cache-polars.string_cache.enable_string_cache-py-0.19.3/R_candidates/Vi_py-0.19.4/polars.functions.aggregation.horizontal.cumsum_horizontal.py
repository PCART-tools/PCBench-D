def cumsum_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr:
    """
    Cumulatively sum all values horizontally across columns.

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
    >>> df.with_columns(pl.cumsum_horizontal("a", "b"))
    shape: (3, 4)
    ┌─────┬──────┬─────┬───────────┐
    │ a   ┆ b    ┆ c   ┆ cumsum    │
    │ --- ┆ ---  ┆ --- ┆ ---       │
    │ i64 ┆ i64  ┆ str ┆ struct[2] │
    ╞═════╪══════╪═════╪═══════════╡
    │ 1   ┆ 4    ┆ x   ┆ {1,5}     │
    │ 8   ┆ 5    ┆ y   ┆ {8,13}    │
    │ 3   ┆ null ┆ z   ┆ {3,null}  │
    └─────┴──────┴─────┴───────────┘

    """
    pyexprs = parse_as_list_of_expressions(*exprs)
    exprs_wrapped = [wrap_expr(e) for e in pyexprs]

    # (Expr): use u32 as that will not cast to float as eagerly
    return F.cumfold(F.lit(0).cast(UInt32), lambda a, b: a + b, exprs_wrapped).alias(
        "cumsum"
    )
