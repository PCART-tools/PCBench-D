def cov(a: str | Expr, b: str | Expr) -> Expr:
    """
    Compute the covariance between two columns/ expressions.

    Parameters
    ----------
    a
        Column name or Expression.
    b
        Column name or Expression.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.cov("a", "b"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 3.0 │
    └─────┘

    """
    if isinstance(a, str):
        a = F.col(a)
    if isinstance(b, str):
        b = F.col(b)
    return wrap_expr(plr.cov(a._pyexpr, b._pyexpr))
