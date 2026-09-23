def _default_index(n):
    from pandas.core.index import RangeIndex
    return RangeIndex(0, n, name=None)
