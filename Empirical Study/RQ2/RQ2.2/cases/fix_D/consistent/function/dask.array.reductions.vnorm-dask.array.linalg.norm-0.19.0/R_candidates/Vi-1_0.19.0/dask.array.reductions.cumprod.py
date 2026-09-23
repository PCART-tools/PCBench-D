@wraps(np.cumprod)
def cumprod(x, axis=None, dtype=None, out=None):
    return cumreduction(np.cumprod, _cumprod_merge, 1, x, axis, dtype, out=out)
