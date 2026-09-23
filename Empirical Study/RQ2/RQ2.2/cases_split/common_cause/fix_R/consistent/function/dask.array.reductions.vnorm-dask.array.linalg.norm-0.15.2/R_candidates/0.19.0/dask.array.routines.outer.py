@wraps(np.outer)
def outer(a, b):
    a = a.flatten()
    b = b.flatten()

    dtype = np.outer(a.dtype.type(), b.dtype.type()).dtype

    return atop(np.outer, "ij", a, "i", b, "j", dtype=dtype)
