def str_join(arr, sep):
    """
    Join lists contained as elements in the Series/Index with
    passed delimiter. Equivalent to :meth:`str.join`.

    Parameters
    ----------
    sep : string
        Delimiter

    Returns
    -------
    joined : Series/Index of objects
    """
    return _na_map(sep.join, arr)
