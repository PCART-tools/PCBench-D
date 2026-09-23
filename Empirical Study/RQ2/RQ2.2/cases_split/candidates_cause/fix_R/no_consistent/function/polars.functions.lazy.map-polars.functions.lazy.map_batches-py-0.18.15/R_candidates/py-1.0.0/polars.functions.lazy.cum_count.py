def cum_count(*columns: str, reverse: bool = False) -> Expr:
    """
    Return the cumulative count of the non-null values in the column.

    This function is syntactic sugar for `col(columns).cum_count()`.

    If no arguments are passed, returns the cumulative count of a context.
    Rows containing null values count towards the result.

    Parameters
    ----------
    *columns
        Name(s) of the columns to use.
    reverse
        Reverse the operation.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 2, None], "b": [3, None, None]})
    >>> df.select(pl.cum_count("a"))
    shape: (3, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 1   │
    │ 2   │
    │ 2   │
    └─────┘
    """
    return F.col(*columns).cum_count(reverse=reverse)
