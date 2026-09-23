def zeros(
    n: int | Expr,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with zeros.

    This is syntactic sugar for the `repeat` function.

    Parameters
    ----------
    n
        Length of the resulting column.
    dtype
        Data type of the resulting column. Defaults to Float64.
    eager
        Evaluate immediately and return a `Series`. If set to `False`,
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
    if (zero := _one_or_zero_by_dtype(0, dtype)) is None:
        msg = f"invalid dtype for `zeros`; found {dtype}"
        raise TypeError(msg)

    return repeat(zero, n=n, dtype=dtype, eager=eager).alias("zeros")
