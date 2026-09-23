def implode(name: str) -> Expr:
    """
    Aggregate all column values into a list.

    Parameters
    ----------
    name
        Name of the column that should be imploded.

    """
    return F.col(name).implode()
