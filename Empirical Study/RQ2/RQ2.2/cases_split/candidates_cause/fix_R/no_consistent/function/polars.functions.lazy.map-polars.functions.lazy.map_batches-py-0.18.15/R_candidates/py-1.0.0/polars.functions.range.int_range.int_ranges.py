def int_ranges(
    start: int | IntoExprColumn = 0,
    end: int | IntoExprColumn | None = None,
    step: int | IntoExprColumn = 1,
    *,
    dtype: PolarsIntegerType = Int64,
    eager: bool = False,
) -> Expr | Series:
    """
    Generate a range of integers for each row of the input columns.

    Parameters
    ----------
    start
        Start of the range (inclusive). Defaults to 0.
    end
        End of the range (exclusive). If set to `None` (default),
        the value of `start` is used and `start` is set to `0`.
    step
        Step size of the range.
    dtype
        Integer data type of the ranges. Defaults to `Int64`.
    eager
        Evaluate immediately and return a `Series`.
        If set to `False` (default), return an expression instead.

    Returns
    -------
    Expr or Series
        Column of data type `List(dtype)`.

    See Also
    --------
    int_range : Generate a single range of integers.

    Examples
    --------
    >>> df = pl.DataFrame({"start": [1, -1], "end": [3, 2]})
    >>> df.with_columns(int_range=pl.int_ranges("start", "end"))
    shape: (2, 3)
    ┌───────┬─────┬────────────┐
    │ start ┆ end ┆ int_range  │
    │ ---   ┆ --- ┆ ---        │
    │ i64   ┆ i64 ┆ list[i64]  │
    ╞═══════╪═════╪════════════╡
    │ 1     ┆ 3   ┆ [1, 2]     │
    │ -1    ┆ 2   ┆ [-1, 0, 1] │
    └───────┴─────┴────────────┘

    `end` can be omitted for a shorter syntax.

    >>> df.select("end", int_range=pl.int_ranges("end"))
    shape: (2, 2)
    ┌─────┬───────────┐
    │ end ┆ int_range │
    │ --- ┆ ---       │
    │ i64 ┆ list[i64] │
    ╞═════╪═══════════╡
    │ 3   ┆ [0, 1, 2] │
    │ 2   ┆ [0, 1]    │
    └─────┴───────────┘
    """
    if end is None:
        end = start
        start = 0

    start = parse_into_expression(start)
    end = parse_into_expression(end)
    step = parse_into_expression(step)
    result = wrap_expr(plr.int_ranges(start, end, step, dtype))

    if eager:
        return F.select(result).to_series()

    return result
