@wraps(np.cumsum)
def cumsum(x, axis=None, dtype=None, out=None):
    return cumreduction(np.cumsum, _cumsum_merge, 0, x, axis, dtype, out=out)
