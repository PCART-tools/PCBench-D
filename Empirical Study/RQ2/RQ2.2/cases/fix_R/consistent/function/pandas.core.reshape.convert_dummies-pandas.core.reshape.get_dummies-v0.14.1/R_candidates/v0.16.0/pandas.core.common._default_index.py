def _default_index(n):
    from pandas.core.index import Int64Index
    values = np.arange(n, dtype=np.int64)
    result = Int64Index(values,name=None)
    result.is_unique = True
    return result
