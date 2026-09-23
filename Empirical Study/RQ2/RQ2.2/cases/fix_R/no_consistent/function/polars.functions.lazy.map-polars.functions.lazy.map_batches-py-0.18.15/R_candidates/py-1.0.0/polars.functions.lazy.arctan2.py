def arctan2(y: str | Expr, x: str | Expr) -> Expr:
    """
    Compute two argument arctan in radians.

    Returns the angle (in radians) in the plane between the
    positive x-axis and the ray from the origin to (x,y).

    Parameters
    ----------
    y
        Column name or Expression.
    x
        Column name or Expression.

    Examples
    --------
    >>> c = (2**0.5) / 2
    >>> df = pl.DataFrame(
    ...     {
    ...         "y": [c, -c, c, -c],
    ...         "x": [c, c, -c, -c],
    ...     }
    ... )
    >>> df.with_columns(pl.arctan2("y", "x").alias("atan2"))
    shape: (4, 3)
    ┌───────────┬───────────┬───────────┐
    │ y         ┆ x         ┆ atan2     │
    │ ---       ┆ ---       ┆ ---       │
    │ f64       ┆ f64       ┆ f64       │
    ╞═══════════╪═══════════╪═══════════╡
    │ 0.707107  ┆ 0.707107  ┆ 0.785398  │
    │ -0.707107 ┆ 0.707107  ┆ -0.785398 │
    │ 0.707107  ┆ -0.707107 ┆ 2.356194  │
    │ -0.707107 ┆ -0.707107 ┆ -2.356194 │
    └───────────┴───────────┴───────────┘
    """
    if isinstance(y, str):
        y = F.col(y)
    if isinstance(x, str):
        x = F.col(x)
    return wrap_expr(plr.arctan2(y._pyexpr, x._pyexpr))
