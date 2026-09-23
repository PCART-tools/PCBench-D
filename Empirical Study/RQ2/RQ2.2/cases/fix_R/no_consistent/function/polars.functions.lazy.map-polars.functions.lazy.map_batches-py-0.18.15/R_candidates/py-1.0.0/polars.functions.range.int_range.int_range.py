def int_range(
    start: int | IntoExprColumn = 0,
    end: int | IntoExprColumn | None = None,
    step: int = 1,
    *,
    dtype: PolarsIntegerType = Int64,
    eager: bool = False,
) -> Expr | Series:
    """
    Generate a range of integers.

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
        Data type of the range.
    eager
        Evaluate immediately and return a `Series`.
        If set to `False` (default), return an expression instead.

    Returns
    -------
    Expr or Series
        Column of integer data type `dtype`.

    See Also
    --------
    int_ranges : Generate a range of integers for each row of the input columns.

    Examples
    --------
    >>> pl.int_range(0, 3, eager=True)
    shape: (3,)
    Series: 'literal' [i64]
    [
            0
            1
            2
    ]

    `end` can be omitted for a shorter syntax.

    >>> pl.int_range(3, eager=True)
    shape: (3,)
    Series: 'literal' [i64]
    [
            0
            1
            2
    ]

    Generate an index column by using `int_range` in conjunction with :func:`len`.

    >>> df = pl.DataFrame({"a": [1, 3, 5], "b": [2, 4, 6]})
    >>> df.select(
    ...     pl.int_range(pl.len(), dtype=pl.UInt32).alias("index"),
    ...     pl.all(),
    ... )
    shape: (3, 3)
    ┌───────┬─────┬─────┐
    │ index ┆ a   ┆ b   │
    │ ---   ┆ --- ┆ --- │
    │ u32   ┆ i64 ┆ i64 │
    ╞═══════╪═════╪═════╡
    │ 0     ┆ 1   ┆ 2   │
    │ 1     ┆ 3   ┆ 4   │
    │ 2     ┆ 5   ┆ 6   │
    └───────┴─────┴─────┘
    """
    if end is None:
        end = start
        start = 0

    if isinstance(start, int) and isinstance(end, int) and eager:
        return wrap_s(plr.eager_int_range(start, end, step, dtype))

    start = parse_into_expression(start)
    end = parse_into_expression(end)
    result = wrap_expr(plr.int_range(start, end, step, dtype))

    if eager:
        return F.select(result).to_series()

    return result
