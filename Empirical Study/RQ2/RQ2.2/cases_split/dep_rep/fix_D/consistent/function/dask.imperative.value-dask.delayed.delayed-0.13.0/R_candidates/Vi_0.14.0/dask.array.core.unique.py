@wraps(np.unique)
def unique(x):
    name = 'unique-' + x.name
    dsk = dict(((name, i), (np.unique, key)) for i, key in enumerate(x._keys()))
    parts = Array._get(sharedict.merge((name, dsk), x.dask), list(dsk.keys()))
    return np.unique(np.concatenate(parts))
