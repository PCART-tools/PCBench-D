def int_range(
    start: int | IntoExpr,
    end: int | IntoExpr,
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
        Lower bound of the range (inclusive).
    end
        Upper bound of the range (exclusive).
    step
        Step size of the range.
    dtype
        Data type of the range. Defaults to ``Int64``.
    eager
        Evaluate immediately and return a ``Series``.
        If set to ``False`` (default), return an expression instead.

    Returns
    -------
    Expr or Series
        Column of data type :class:`Int64`.

    See Also
    --------
    int_ranges : Generate a range of integers for each row of the input columns.

    Examples
    --------
    >>> pl.int_range(0, 3, eager=True)
    shape: (3,)
    Series: 'int' [i64]
    [
            0
            1
            2
    ]

    """
    start = parse_as_expression(start)
    end = parse_as_expression(end)
    result = wrap_expr(plr.int_range(start, end, step, dtype))

    if eager:
        return F.select(result).to_series()

    return result
