def concat_list(exprs: IntoExpr | Iterable[IntoExpr], *more_exprs: IntoExpr) -> Expr:
    """
    Horizontally concatenate columns into a single list column.

    Operates in linear time.

    Parameters
    ----------
    exprs
        Columns to concatenate into a single list column. Accepts expression input.
        Strings are parsed as column names, other non-expression inputs are parsed as
        literals.
    *more_exprs
        Additional columns to concatenate into a single list column, specified as
        positional arguments.

    Examples
    --------
    Concatenate two existing list columns. Null values are propagated.

    >>> df = pl.DataFrame({"a": [[1, 2], [3], [4, 5]], "b": [[4], [], None]})
    >>> df.with_columns(concat_list=pl.concat_list("a", "b"))
    shape: (3, 3)
    ┌───────────┬───────────┬─────────────┐
    │ a         ┆ b         ┆ concat_list │
    │ ---       ┆ ---       ┆ ---         │
    │ list[i64] ┆ list[i64] ┆ list[i64]   │
    ╞═══════════╪═══════════╪═════════════╡
    │ [1, 2]    ┆ [4]       ┆ [1, 2, 4]   │
    │ [3]       ┆ []        ┆ [3]         │
    │ [4, 5]    ┆ null      ┆ null        │
    └───────────┴───────────┴─────────────┘

    Non-list columns are cast to a list before concatenation. The output data type
    is the supertype of the concatenated columns.

    >>> df.select("a", concat_list=pl.concat_list("a", pl.lit("x")))
    shape: (3, 2)
    ┌───────────┬─────────────────┐
    │ a         ┆ concat_list     │
    │ ---       ┆ ---             │
    │ list[i64] ┆ list[str]       │
    ╞═══════════╪═════════════════╡
    │ [1, 2]    ┆ ["1", "2", "x"] │
    │ [3]       ┆ ["3", "x"]      │
    │ [4, 5]    ┆ ["4", "5", "x"] │
    └───────────┴─────────────────┘

    Create lagged columns and collect them into a list. This mimics a rolling window.

    >>> df = pl.DataFrame({"A": [1.0, 2.0, 9.0, 2.0, 13.0]})
    >>> df = df.select([pl.col("A").shift(i).alias(f"A_lag_{i}") for i in range(3)])
    >>> df.select(
    ...     pl.concat_list([f"A_lag_{i}" for i in range(3)][::-1]).alias("A_rolling")
    ... )
    shape: (5, 1)
    ┌───────────────────┐
    │ A_rolling         │
    │ ---               │
    │ list[f64]         │
    ╞═══════════════════╡
    │ [null, null, 1.0] │
    │ [null, 1.0, 2.0]  │
    │ [1.0, 2.0, 9.0]   │
    │ [2.0, 9.0, 2.0]   │
    │ [9.0, 2.0, 13.0]  │
    └───────────────────┘
    """
    exprs = parse_into_list_of_expressions(exprs, *more_exprs)
    return wrap_expr(plr.concat_list(exprs))
