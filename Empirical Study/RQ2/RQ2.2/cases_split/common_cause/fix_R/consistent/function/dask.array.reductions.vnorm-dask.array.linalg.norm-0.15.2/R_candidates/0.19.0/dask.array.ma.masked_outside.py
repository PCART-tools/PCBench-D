@wraps(np.ma.masked_outside)
def masked_outside(x, v1, v2):
    x = asanyarray(x)
    return x.map_blocks(np.ma.masked_outside, v1, v2)
