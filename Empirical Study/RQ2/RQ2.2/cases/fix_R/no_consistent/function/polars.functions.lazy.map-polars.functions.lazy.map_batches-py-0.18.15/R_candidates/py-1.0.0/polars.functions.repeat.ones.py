def ones(
    n: int | Expr,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with ones.

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
    >>> pl.ones(3, pl.Int8, eager=True)
    shape: (3,)
    Series: 'ones' [i8]
    [
        1
        1
        1
    ]
    """
    if (one := _one_or_zero_by_dtype(1, dtype)) is None:
        msg = f"invalid dtype for `ones`; found {dtype}"
        raise TypeError(msg)

    return repeat(one, n=n, dtype=dtype, eager=eager).alias("ones")
