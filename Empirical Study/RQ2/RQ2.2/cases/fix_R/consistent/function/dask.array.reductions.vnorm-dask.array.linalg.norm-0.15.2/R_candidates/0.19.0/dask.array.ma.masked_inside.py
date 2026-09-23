@wraps(np.ma.masked_inside)
def masked_inside(x, v1, v2):
    x = asanyarray(x)
    return x.map_blocks(np.ma.masked_inside, v1, v2)
