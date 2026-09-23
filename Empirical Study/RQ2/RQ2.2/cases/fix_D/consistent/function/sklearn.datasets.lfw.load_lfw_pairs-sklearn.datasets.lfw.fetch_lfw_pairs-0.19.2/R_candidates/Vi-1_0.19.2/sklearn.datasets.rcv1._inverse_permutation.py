def _inverse_permutation(p):
    """inverse permutation p"""
    n = p.size
    s = np.zeros(n, dtype=np.int32)
    i = np.arange(n, dtype=np.int32)
    np.put(s, p, i)  # s[p] = i
    return s
