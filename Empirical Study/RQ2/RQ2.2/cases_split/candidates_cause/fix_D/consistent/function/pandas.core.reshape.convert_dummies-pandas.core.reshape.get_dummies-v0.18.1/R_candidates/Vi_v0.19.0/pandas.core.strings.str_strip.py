def str_strip(arr, to_strip=None, side='both'):
    """
    Strip whitespace (including newlines) from each string in the
    Series/Index.

    Parameters
    ----------
    to_strip : str or unicode
    side : {'left', 'right', 'both'}, default 'both'

    Returns
    -------
    stripped : Series/Index of objects
    """
    if side == 'both':
        f = lambda x: x.strip(to_strip)
    elif side == 'left':
        f = lambda x: x.lstrip(to_strip)
    elif side == 'right':
        f = lambda x: x.rstrip(to_strip)
    else:  # pragma: no cover
        raise ValueError('Invalid side')
    return _na_map(f, arr)
