@wraps(np.ma.set_fill_value)
def set_fill_value(a, fill_value):
    a = asanyarray(a)
    if getattr(fill_value, 'shape', ()):
        raise ValueError("da.ma.set_fill_value doesn't support array `value`s")
    fill_value = np.ma.core._check_fill_value(fill_value, a.dtype)
    res = a.map_blocks(_set_fill_value, fill_value)
    a.dask = res.dask
    a.name = res.name
