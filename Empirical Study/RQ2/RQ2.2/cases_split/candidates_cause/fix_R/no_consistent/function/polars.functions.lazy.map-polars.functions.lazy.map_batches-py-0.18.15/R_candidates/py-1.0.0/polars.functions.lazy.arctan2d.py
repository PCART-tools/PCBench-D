@deprecate_function("Use `arctan2` followed by `.degrees()` instead.", version="1.0.0")
def arctan2d(y: str | Expr, x: str | Expr) -> Expr:
    """
    Compute two argument arctan in degrees.

    .. deprecated:: 1.0.0
        Use `arctan2` followed by :meth:`Expr.degrees` instead.

    Returns the angle (in degrees) in the plane between the positive x-axis
    and the ray from the origin to (x,y).

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
    >>> df.select(  # doctest: +SKIP
    ...     pl.arctan2d("y", "x").alias("atan2d"),
    ...     pl.arctan2("y", "x").alias("atan2"),
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
    return arctan2(y, x).degrees()
