def binary() -> SelectorType:
    """
    Select all binary columns.

    See Also
    --------
    by_dtype : Select all columns matching the given dtype(s).
    string : Select all string columns (optionally including categoricals).

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame({"a": [b"hello"], "b": ["world"], "c": [b"!"], "d": [":)"]})
    >>> df
    shape: (1, 4)
    ┌───────────────┬───────┬───────────────┬─────┐
    │ a             ┆ b     ┆ c             ┆ d   │
    │ ---           ┆ ---   ┆ ---           ┆ --- │
    │ binary        ┆ str   ┆ binary        ┆ str │
    ╞═══════════════╪═══════╪═══════════════╪═════╡
    │ [binary data] ┆ world ┆ [binary data] ┆ :)  │
    └───────────────┴───────┴───────────────┴─────┘

    Select binary columns and export as a dict:

    >>> df.select(cs.binary()).to_dict(False)
    {'a': [b'hello'], 'c': [b'!']}

    Select all columns *except* for those that are binary:

    >>> df.select(~cs.binary()).to_dict(False)
    {'b': ['world'], 'd': [':)']}

    """
    return _selector_proxy_(F.col(Binary), name="binary")
