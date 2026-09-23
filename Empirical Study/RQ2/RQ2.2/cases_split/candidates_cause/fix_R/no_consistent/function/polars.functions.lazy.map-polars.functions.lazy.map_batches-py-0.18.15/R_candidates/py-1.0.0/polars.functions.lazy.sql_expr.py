def sql_expr(sql: str | Sequence[str]) -> Expr | list[Expr]:
    """
    Parse one or more SQL expressions to Polars expression(s).

    Parameters
    ----------
    sql
        One or more SQL expressions.

    Examples
    --------
    Parse a single SQL expression:

    >>> df = pl.DataFrame({"a": [2, 1]})
    >>> expr = pl.sql_expr("MAX(a)")
    >>> df.select(expr)
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 2   │
    └─────┘

    Parse multiple SQL expressions:

    >>> df.with_columns(
    ...     *pl.sql_expr(["POWER(a,a) AS a_a", "CAST(a AS TEXT) AS a_txt"]),
    ... )
    shape: (2, 3)
    ┌─────┬─────┬───────┐
    │ a   ┆ a_a ┆ a_txt │
    │ --- ┆ --- ┆ ---   │
    │ i64 ┆ i64 ┆ str   │
    ╞═════╪═════╪═══════╡
    │ 2   ┆ 4   ┆ 2     │
    │ 1   ┆ 1   ┆ 1     │
    └─────┴─────┴───────┘
    """
    if isinstance(sql, str):
        return wrap_expr(plr.sql_expr(sql))
    else:
        return [wrap_expr(plr.sql_expr(q)) for q in sql]
