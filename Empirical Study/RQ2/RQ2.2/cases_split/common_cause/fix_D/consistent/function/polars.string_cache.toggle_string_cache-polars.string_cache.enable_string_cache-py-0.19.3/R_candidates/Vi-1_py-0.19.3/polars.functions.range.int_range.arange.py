def arange(
    start: int | IntoExpr,
    end: int | IntoExpr,
    step: int = 1,
    *,
    dtype: PolarsIntegerType = Int64,
    eager: bool = False,
) -> Expr | Series:
    """
    Generate a range of integers.

    Alias for :func:`int_range`.

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
    Column of data type ``dtype``.

    See Also
    --------
    int_range : Generate a range of integers.
    int_ranges : Generate a range of integers for each row of the input columns.

    Examples
    --------
    >>> pl.arange(0, 3, eager=True)
    shape: (3,)
    Series: 'int' [i64]
    [
            0
            1
            2
    ]

    """
    return int_range(start, end, step, dtype=dtype, eager=eager)
