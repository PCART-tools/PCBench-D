def _expand_selectors(
    frame: DataFrame | LazyFrame, items: Any, *more_items: Any
) -> list[Any]:
    """
    Internal function that expands any selectors to column names in the given input.

    Non-selector values are left as-is.

    Examples
    --------
    >>> from polars.selectors import _expand_selectors
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "colw": ["a", "b"],
    ...         "colx": ["x", "y"],
    ...         "coly": [123, 456],
    ...         "colz": [2.0, 5.5],
    ...     }
    ... )
    >>> _expand_selectors(df, ["colx", cs.numeric()])
    ['colx', 'coly', 'colz']
    >>> _expand_selectors(df, cs.string(), cs.float())
    ['colw', 'colx', 'colz']

    """
    expanded: list[Any] = []
    for item in (
        *(
            items
            if isinstance(items, Collection) and not isinstance(items, str)
            else [items]
        ),
        *more_items,
    ):
        if is_selector(item):
            selector_cols = expand_selector(frame, item)
            expanded.extend(selector_cols)
        else:
            expanded.append(item)
    return expanded
