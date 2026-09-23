def str_find(arr, sub, start=0, end=None, side='left'):
    """
    Return indexes in each strings where the substring is
    fully contained between [start:end]. Return -1 on failure.

    Parameters
    ----------
    sub : str
        Substring being searched
    start : int
        Left edge index
    end : int
        Right edge index
    side : {'left', 'right'}, default 'left'
        Specifies a starting side, equivalent to ``find`` or ``rfind``

    Returns
    -------
    found : array
    """

    if not isinstance(sub, compat.string_types):
        msg = 'expected a string object, not {0}'
        raise TypeError(msg.format(type(sub).__name__))

    if side == 'left':
        method = 'find'
    elif side == 'right':
        method = 'rfind'
    else:  # pragma: no cover
        raise ValueError('Invalid side')

    if end is None:
        f = lambda x: getattr(x, method)(sub, start)
    else:
        f = lambda x: getattr(x, method)(sub, start, end)

    return _na_map(f, arr, dtype=int)
