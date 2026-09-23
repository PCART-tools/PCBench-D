@wraps(np.diff)
def diff(a, n=1, axis=-1):
    a = asarray(a)
    n = int(n)
    axis = int(axis)

    sl_1 = a.ndim * [slice(None)]
    sl_2 = a.ndim * [slice(None)]

    sl_1[axis] = slice(1, None)
    sl_2[axis] = slice(None, -1)

    sl_1 = tuple(sl_1)
    sl_2 = tuple(sl_2)

    r = a
    for i in range(n):
        r = r[sl_1] - r[sl_2]

    return r
