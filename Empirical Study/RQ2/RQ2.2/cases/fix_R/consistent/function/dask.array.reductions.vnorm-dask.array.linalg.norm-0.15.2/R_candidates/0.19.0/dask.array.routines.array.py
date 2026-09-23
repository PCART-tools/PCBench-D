@wraps(np.array)
def array(x, dtype=None, ndmin=None):
    while ndmin is not None and x.ndim < ndmin:
        x = x[None, :]
    if dtype is not None and x.dtype != dtype:
        x = x.astype(dtype)
    return x
