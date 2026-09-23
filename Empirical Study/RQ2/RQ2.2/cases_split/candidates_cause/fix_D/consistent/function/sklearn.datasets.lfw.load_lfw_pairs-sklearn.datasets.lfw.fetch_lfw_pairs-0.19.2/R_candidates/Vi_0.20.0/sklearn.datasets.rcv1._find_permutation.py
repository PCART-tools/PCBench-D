def _find_permutation(a, b):
    """find the permutation from a to b"""
    t = np.argsort(a)
    u = np.argsort(b)
    u_ = _inverse_permutation(u)
    return t[u_]
