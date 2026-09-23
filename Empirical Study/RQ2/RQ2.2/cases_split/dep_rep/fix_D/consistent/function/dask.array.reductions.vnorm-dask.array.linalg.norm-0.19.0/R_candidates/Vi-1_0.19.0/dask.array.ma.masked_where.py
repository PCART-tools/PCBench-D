@wraps(np.ma.masked_where)
def masked_where(condition, a):
    cshape = getattr(condition, 'shape', ())
    if cshape and cshape != a.shape:
        raise IndexError("Inconsistant shape between the condition and the "
                         "input (got %s and %s)" % (cshape, a.shape))
    condition = asanyarray(condition)
    a = asanyarray(a)
    ainds = tuple(range(a.ndim))
    cinds = tuple(range(condition.ndim))
    return atop(np.ma.masked_where, ainds, condition, cinds, a, ainds,
                dtype=a.dtype)
