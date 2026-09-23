def int_ranges(
    start: IntoExpr,
    end: IntoExpr,
    step: int = 1,
    *,
    dtype: PolarsIntegerType = Int64,
    eager: bool = False,
) -> Expr | Series:
    """
    Generate a range of integers for each row of the input columns.

    Parameters
    ----------
    start
        Lower bound of the range (inclusive).
    end
        Upper bound of the range (exclusive).
    step
        Step size of the range.
    dtype
        Integer data type of the ranges. Defaults to ``Int64``.
    eager
        Evaluate immediately and return a ``Series``.
        If set to ``False`` (default), return an expression instead.

    Returns
    -------
    Expr or Series
        Column of data type ``List(dtype)``.

    See Also
    --------
    int_range : Generate a single range of integers.

    Examples
    --------
    >>> df = pl.DataFrame({"start": [1, -1], "end": [3, 2]})
    >>> df.with_columns(pl.int_ranges("start", "end"))
    shape: (2, 3)
    ┌───────┬─────┬────────────┐
    │ start ┆ end ┆ int_range  │
    │ ---   ┆ --- ┆ ---        │
    │ i64   ┆ i64 ┆ list[i64]  │
    ╞═══════╪═════╪════════════╡
    │ 1     ┆ 3   ┆ [1, 2]     │
    │ -1    ┆ 2   ┆ [-1, 0, 1] │
    └───────┴─────┴────────────┘

    """
    start = parse_as_expression(start)
    end = parse_as_expression(end)
    result = wrap_expr(plr.int_ranges(start, end, step, dtype))

    if eager:
        return F.select(result).to_series()

    return result
