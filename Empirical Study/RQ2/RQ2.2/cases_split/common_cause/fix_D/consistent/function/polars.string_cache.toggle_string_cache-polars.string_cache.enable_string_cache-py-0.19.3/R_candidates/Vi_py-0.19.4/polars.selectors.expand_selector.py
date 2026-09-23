def expand_selector(
    target: DataFrame | LazyFrame | Mapping[str, PolarsDataType], selector: SelectorType
) -> tuple[str, ...]:
    """
    Expand a selector to column names with respect to a specific frame or schema target.

    Parameters
    ----------
    target
        A polars DataFrame, LazyFrame or schema.
    selector
        An arbitrary polars selector (or compound selector).

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "colx": ["a", "b", "c"],
    ...         "coly": [123, 456, 789],
    ...         "colz": [2.0, 5.5, 8.0],
    ...     }
    ... )

    Expand selector with respect to an existing `DataFrame`:

    >>> cs.expand_selector(df, cs.numeric())
    ('coly', 'colz')
    >>> cs.expand_selector(df, cs.first() | cs.last())
    ('colx', 'colz')

    This also works with `LazyFrame`:

    >>> cs.expand_selector(df.lazy(), ~(cs.first() | cs.last()))
    ('coly',)

    Expand selector with respect to a standalone schema:

    >>> schema = {
    ...     "colx": pl.Float32,
    ...     "coly": pl.Float64,
    ...     "colz": pl.Date,
    ... }
    >>> cs.expand_selector(schema, cs.float())
    ('colx', 'coly')

    """
    if isinstance(target, Mapping):
        from polars.dataframe import DataFrame

        target = DataFrame(schema=target)

    return tuple(target.select(selector).columns)
