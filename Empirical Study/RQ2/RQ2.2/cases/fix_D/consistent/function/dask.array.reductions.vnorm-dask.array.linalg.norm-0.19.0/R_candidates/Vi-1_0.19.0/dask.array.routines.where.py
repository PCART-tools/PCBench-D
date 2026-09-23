@wraps(np.where)
def where(condition, x=None, y=None):
    if (x is None) != (y is None):
        raise ValueError("either both or neither of x and y should be given")
    if (x is None) and (y is None):
        return nonzero(condition)

    if np.isscalar(condition):
        dtype = result_type(x, y)
        x = asarray(x)
        y = asarray(y)

        shape = broadcast_shapes(x.shape, y.shape)
        out = x if condition else y

        return broadcast_to(out, shape).astype(dtype)
    else:
        return elemwise(np.where, condition, x, y)
