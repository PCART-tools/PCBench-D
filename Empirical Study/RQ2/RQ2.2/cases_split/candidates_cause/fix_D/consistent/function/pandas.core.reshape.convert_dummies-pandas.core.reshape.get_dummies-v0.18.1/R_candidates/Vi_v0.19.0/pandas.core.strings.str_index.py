def str_index(arr, sub, start=0, end=None, side='left'):
    if not isinstance(sub, compat.string_types):
        msg = 'expected a string object, not {0}'
        raise TypeError(msg.format(type(sub).__name__))

    if side == 'left':
        method = 'index'
    elif side == 'right':
        method = 'rindex'
    else:  # pragma: no cover
        raise ValueError('Invalid side')

    if end is None:
        f = lambda x: getattr(x, method)(sub, start)
    else:
        f = lambda x: getattr(x, method)(sub, start, end)

    return _na_map(f, arr, dtype=int)
