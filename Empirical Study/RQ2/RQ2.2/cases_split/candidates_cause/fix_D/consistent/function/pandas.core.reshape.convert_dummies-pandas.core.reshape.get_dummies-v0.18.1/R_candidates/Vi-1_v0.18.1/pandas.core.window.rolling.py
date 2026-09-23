def rolling(obj, win_type=None, **kwds):
    from pandas import Series, DataFrame
    if not isinstance(obj, (Series, DataFrame)):
        raise TypeError('invalid type: %s' % type(obj))

    if win_type is not None:
        return Window(obj, win_type=win_type, **kwds)

    return Rolling(obj, **kwds)
