def any(*names: str, ignore_nulls: bool = True) -> Expr | bool | None:
    """
    Evaluate a bitwise OR operation.

    Syntactic sugar for `col(names).any()`.

    See Also
    --------
    any_horizontal

    Parameters
    ----------
    *names
        Name(s) of the columns to use in the aggregation.
    ignore_nulls
        Ignore null values (default).

        If set to `False`, `Kleene logic`_ is used to deal with nulls:
        if the column contains any null values and no `True` values,
        the output is null.

        .. _Kleene logic: https://en.wikipedia.org/wiki/Three-valued_logic

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [True, False, True],
    ...         "b": [False, False, False],
    ...     }
    ... )
    >>> df.select(pl.any("a"))
    shape: (1, 1)
    ┌──────┐
    │ a    │
    │ ---  │
    │ bool │
    ╞══════╡
    │ true │
    └──────┘
    """
    return F.col(*names).any(ignore_nulls=ignore_nulls)
