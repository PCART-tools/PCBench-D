def dict_to_numpy_array1(d, mapping=None):
    """Convert a dictionary of numbers to a 1d numpy array
    with optional mapping.

    """
    if mapping is None:
        s = set(d.keys())
        mapping = dict(zip(s, range(len(s))))
    n = len(mapping)
    a = np.zeros(n)
    for k1, i in mapping.items():
        i = mapping[k1]
        a[i] = d[k1]
    return a
