def groups(column: str) -> Expr:
    """Syntactic sugar for `pl.col("foo").agg_groups()`."""
    return F.col(column).agg_groups()
