def rolling_cov(
    a: str | Expr,
    b: str | Expr,
    *,
    window_size: int,
    min_periods: int | None = None,
    ddof: int = 1,
) -> Expr:
    """
    Compute the rolling covariance between two columns/ expressions.

    The window at a given row includes the row itself and the
    `window_size - 1` elements before it.

    Parameters
    ----------
    a
        Column name or Expression.
    b
        Column name or Expression.
    window_size
        The length of the window.
    min_periods
        The number of values in the window that should be non-null before computing
        a result. If None, it will be set equal to window size.
    ddof
        Delta degrees of freedom.  The divisor used in calculations
        is ``N - ddof``, where ``N`` represents the number of elements.

    """
    if min_periods is None:
        min_periods = window_size
    if isinstance(a, str):
        a = F.col(a)
    if isinstance(b, str):
        b = F.col(b)
    return wrap_expr(
        plr.rolling_cov(a._pyexpr, b._pyexpr, window_size, min_periods, ddof)
    )
