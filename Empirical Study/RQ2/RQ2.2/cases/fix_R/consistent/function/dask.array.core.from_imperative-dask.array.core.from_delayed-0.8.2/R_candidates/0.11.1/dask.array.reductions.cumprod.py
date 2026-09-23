@wraps(np.cumprod)
def cumprod(x, axis, dtype=None):
    return cumreduction(np.cumprod, operator.mul, 1, x, axis, dtype)
