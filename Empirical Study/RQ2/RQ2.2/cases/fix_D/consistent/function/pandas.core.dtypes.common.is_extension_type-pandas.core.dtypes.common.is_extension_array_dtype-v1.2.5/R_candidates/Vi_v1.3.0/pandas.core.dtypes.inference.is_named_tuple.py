def is_named_tuple(obj) -> bool:
    """
    Check if the object is a named tuple.

    Parameters
    ----------
    obj : The object to check

    Returns
    -------
    is_named_tuple : bool
        Whether `obj` is a named tuple.

    Examples
    --------
    >>> from collections import namedtuple
    >>> Point = namedtuple("Point", ["x", "y"])
    >>> p = Point(1, 2)
    >>>
    >>> is_named_tuple(p)
    True
    >>> is_named_tuple((1, 2))
    False
    """
    return isinstance(obj, tuple) and hasattr(obj, "_fields")
