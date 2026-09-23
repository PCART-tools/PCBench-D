@wraps(np.ma.fix_invalid)
def fix_invalid(a, fill_value=None):
    a = asanyarray(a)
    return a.map_blocks(np.ma.fix_invalid, fill_value=fill_value)
