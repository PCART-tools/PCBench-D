@wraps(np.cumsum)
def cumsum(x, axis, dtype=None):
    return cumreduction(np.cumsum, operator.add, 0, x, axis, dtype)
