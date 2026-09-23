def str_pad(arr, width, side='left', fillchar=' '):
    """
    Pad strings with an additional character

    Parameters
    ----------
    arr : list or array-like
    width : int
        Minimum width of resulting string; additional characters will be filled
        with spaces
    side : {'left', 'right', 'both'}, default 'left'
    fillchar : str
        Additional character for filling, default is whitespace

    Returns
    -------
    padded : array
    """

    if not isinstance(fillchar, compat.string_types):
        msg = 'fillchar must be a character, not {0}'
        raise TypeError(msg.format(type(fillchar).__name__))

    if len(fillchar) != 1:
        raise TypeError('fillchar must be a character, not str')

    if side == 'left':
        f = lambda x: x.rjust(width, fillchar)
    elif side == 'right':
        f = lambda x: x.ljust(width, fillchar)
    elif side == 'both':
        f = lambda x: x.center(width, fillchar)
    else:  # pragma: no cover
        raise ValueError('Invalid side')

    return _na_map(f, arr)
