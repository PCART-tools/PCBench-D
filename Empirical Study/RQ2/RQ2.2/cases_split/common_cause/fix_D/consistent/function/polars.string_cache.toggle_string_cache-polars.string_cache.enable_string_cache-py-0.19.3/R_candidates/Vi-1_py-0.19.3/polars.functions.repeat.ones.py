def ones(
    n: int | Expr,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with ones.

    Syntactic sugar for ``repeat(1.0, ...)``.

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
    >>> pl.ones(3, pl.Int8, eager=True)
    shape: (3,)
    Series: 'ones' [i8]
    [
        1
        1
        1
    ]

    """
    return repeat(1.0, n=n, dtype=dtype, eager=eager).alias("ones")
