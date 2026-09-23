@wraps(np.swapaxes)
def swapaxes(a, axis1, axis2):
    if axis1 == axis2:
        return a
    ind = list(range(a.ndim))
    out = list(ind)
    out[axis1], out[axis2] = axis2, axis1

    return atop(np.swapaxes, out, a, ind, axis1=axis1, axis2=axis2,
                dtype=a._dtype)
