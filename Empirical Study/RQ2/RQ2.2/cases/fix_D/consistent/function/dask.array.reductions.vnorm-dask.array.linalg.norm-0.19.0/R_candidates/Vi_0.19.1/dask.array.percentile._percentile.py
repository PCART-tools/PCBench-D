@wraps(np.percentile)
def _percentile(a, q, interpolation='linear'):
    n = len(a)
    if not len(a):
        return None, n
    if isinstance(q, Iterator):
        q = list(q)
    if a.dtype.name == 'category':
        result = np.percentile(a.codes, q, interpolation=interpolation)
        import pandas as pd
        return pd.Categorical.from_codes(result, a.categories, a.ordered), n
    if np.issubdtype(a.dtype, np.datetime64):
        a2 = a.astype('i8')
        result = np.percentile(a2, q, interpolation=interpolation)
        return result.astype(a.dtype), n
    if not np.issubdtype(a.dtype, np.number):
        interpolation = 'nearest'
    return np.percentile(a, q, interpolation=interpolation), n
