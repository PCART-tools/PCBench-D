@wraps(np.ma.masked_values)
def masked_values(x, value, rtol=1e-05, atol=1e-08, shrink=True):
    x = asanyarray(x)
    if getattr(value, 'shape', ()):
        raise ValueError("da.ma.masked_values doesn't support array `value`s")
    return map_blocks(np.ma.masked_values, x, value, rtol=rtol,
                      atol=atol, shrink=shrink)
