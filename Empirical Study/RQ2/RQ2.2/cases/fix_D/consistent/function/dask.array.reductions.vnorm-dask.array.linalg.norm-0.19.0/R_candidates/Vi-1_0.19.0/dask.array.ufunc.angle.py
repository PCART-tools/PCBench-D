@copy_docstring(source=np.angle)
def angle(x, deg=0):
    deg = bool(deg)
    if hasattr(x, '_elemwise'):
        return x._elemwise(__array_wrap__, np.angle, x, deg)
    return np.angle(x, deg=deg)
