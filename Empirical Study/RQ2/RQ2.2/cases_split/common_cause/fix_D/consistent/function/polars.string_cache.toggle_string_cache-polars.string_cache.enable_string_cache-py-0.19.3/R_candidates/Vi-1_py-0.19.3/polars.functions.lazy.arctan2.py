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
    >>> import math
    >>> twoRootTwo = math.sqrt(2) / 2
    >>> df = pl.DataFrame(
    ...     {
    ...         "y": [twoRootTwo, -twoRootTwo, twoRootTwo, -twoRootTwo],
    ...         "x": [twoRootTwo, twoRootTwo, -twoRootTwo, -twoRootTwo],
    ...     }
    ... )
    >>> df.select(
    ...     pl.arctan2d("y", "x").alias("atan2d"), pl.arctan2("y", "x").alias("atan2")
    ... )
    shape: (4, 2)
    ┌────────┬───────────┐
    │ atan2d ┆ atan2     │
    │ ---    ┆ ---       │
    │ f64    ┆ f64       │
    ╞════════╪═══════════╡
    │ 45.0   ┆ 0.785398  │
    │ -45.0  ┆ -0.785398 │
    │ 135.0  ┆ 2.356194  │
    │ -135.0 ┆ -2.356194 │
    └────────┴───────────┘

    """
    if isinstance(y, str):
        y = F.col(y)
    if isinstance(x, str):
        x = F.col(x)
    return wrap_expr(plr.arctan2(y._pyexpr, x._pyexpr))
