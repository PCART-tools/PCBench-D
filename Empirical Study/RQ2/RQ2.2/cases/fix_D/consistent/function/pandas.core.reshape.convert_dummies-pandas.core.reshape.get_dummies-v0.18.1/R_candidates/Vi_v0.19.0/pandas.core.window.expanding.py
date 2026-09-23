def expanding(obj, **kwds):
    from pandas import Series, DataFrame
    if not isinstance(obj, (Series, DataFrame)):
        raise TypeError('invalid type: %s' % type(obj))

    return Expanding(obj, **kwds)
