@wraps(np.ma.filled)
def filled(a, fill_value=None):
    a = asanyarray(a)
    return a.map_blocks(np.ma.filled, fill_value=fill_value)
