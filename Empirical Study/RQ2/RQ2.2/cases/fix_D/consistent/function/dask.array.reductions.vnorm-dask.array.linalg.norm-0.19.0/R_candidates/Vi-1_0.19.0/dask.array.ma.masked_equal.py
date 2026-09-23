@wraps(np.ma.masked_equal)
def masked_equal(a, value):
    a = asanyarray(a)
    if getattr(value, 'shape', ()):
        raise ValueError("da.ma.masked_equal doesn't support array `value`s")
    inds = tuple(range(a.ndim))
    return atop(np.ma.masked_equal, inds, a, inds, value, (), dtype=a.dtype)
