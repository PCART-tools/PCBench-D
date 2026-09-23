@wraps(np.swapaxes)
def swapaxes(a, axis1, axis2):
    if axis1 == axis2:
        return a
    if axis1 < 0:
        axis1 = axis1 + a.ndim
    if axis2 < 0:
        axis2 = axis2 + a.ndim
    ind = list(range(a.ndim))
    out = list(ind)
    out[axis1], out[axis2] = axis2, axis1

    return atop(np.swapaxes, out, a, ind, axis1=axis1, axis2=axis2,
                dtype=a.dtype)
