@wraps(np.count_nonzero)
def count_nonzero(a, axis=None):
    return isnonzero(asarray(a)).astype(np.intp).sum(axis=axis)
