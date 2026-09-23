def cum_fold(
    acc: IntoExpr,
    function: Callable[[Series, Series], Series],
    exprs: Sequence[Expr | str] | Expr,
    *,
    include_init: bool = False,
) -> Expr:
    """
    Cumulatively fold horizontally across columns with a left fold.

    Every cumulative result is added as a separate field in a Struct column.

    Parameters
    ----------
    acc
        Accumulator expression. This is the value that will be initialized when the fold
        starts. For a sum this could for instance be lit(0).
    function
        Function to apply over the accumulator and the value.
        Fn(acc, value) -> new_value
    exprs
        Expressions to aggregate over. May also be a wildcard expression.
    include_init
        Include the initial accumulator state as struct field.

    Notes
    -----
    If you simply want the first encountered expression as accumulator,
    consider using :func:`cum_reduce`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 2, 3],
    ...         "b": [3, 4, 5],
    ...         "c": [5, 6, 7],
    ...     }
    ... )
    >>> df.with_columns(
    ...     pl.cum_fold(acc=pl.lit(1), function=lambda acc, x: acc + x, exprs=pl.all())
    ... )
    shape: (3, 4)
    ┌─────┬─────┬─────┬───────────┐
    │ a   ┆ b   ┆ c   ┆ cum_fold  │
    │ --- ┆ --- ┆ --- ┆ ---       │
    │ i64 ┆ i64 ┆ i64 ┆ struct[3] │
    ╞═════╪═════╪═════╪═══════════╡
    │ 1   ┆ 3   ┆ 5   ┆ {2,5,10}  │
    │ 2   ┆ 4   ┆ 6   ┆ {3,7,13}  │
    │ 3   ┆ 5   ┆ 7   ┆ {4,9,16}  │
    └─────┴─────┴─────┴───────────┘
    """
    # in case of col("*")
    acc = parse_into_expression(acc, str_as_lit=True)
    if isinstance(exprs, pl.Expr):
        exprs = [exprs]

    exprs = parse_into_list_of_expressions(exprs)
    return wrap_expr(plr.cum_fold(acc, function, exprs, include_init).alias("cum_fold"))
