def is_selector(obj: Any) -> bool:
    """
    Indicate whether the given object/expression is a selector.

    Examples
    --------
    >>> from polars.selectors import is_selector
    >>> import polars.selectors as cs
    >>> is_selector(pl.col("colx"))
    False
    >>> is_selector(cs.first() | cs.last())
    True
    """
    # note: don't want to expose the "_selector_proxy_" object
    return isinstance(obj, _selector_proxy_)
