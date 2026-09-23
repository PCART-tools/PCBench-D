def to_tuple(x):
    """Converts lists to tuples.

    .. deprecated:: 2.8

       to_tuple is deprecated and will be removed in NetworkX 3.0.

    Examples
    --------
    >>> from networkx.utils import to_tuple
    >>> a_list = [1, 2, [1, 4]]
    >>> to_tuple(a_list)
    (1, 2, (1, 4))
    """
    warnings.warn(
        "to_tuple is deprecated and will be removed in NetworkX 3.0.",
        DeprecationWarning,
        stacklevel=2,
    )

    if not isinstance(x, (tuple, list)):
        return x
    return tuple(map(to_tuple, x))
