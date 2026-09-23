@wraps(np.ma.masked_invalid)
def masked_invalid(a):
    return asanyarray(a).map_blocks(np.ma.masked_invalid)
