def zeros(
    n: int | Expr,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with zeros.

    Syntactic sugar for ``repeat(0.0, ...)``.

    Parameters
    ----------
    n
        Length of the resulting column.
    dtype
        Data type of the resulting column. Defaults to Float64.
    eager
        Evaluate immediately and return a ``Series``. If set to ``False``,
        return an expression instead.

    Notes
    -----
    If you want to construct a column in lazy mode and do not need a pre-determined
    length, use :func:`lit` instead.

    See Also
    --------
    repeat
    lit

    Examples
    --------
    >>> pl.zeros(3, pl.Int8, eager=True)
    shape: (3,)
    Series: 'zeros' [i8]
    [
        0
        0
        0
    ]

    """
    return repeat(0.0, n=n, dtype=dtype, eager=eager).alias("zeros")
