@wraps(np.ma.getmaskarray)
def getmaskarray(a):
    a = asanyarray(a)
    return a.map_blocks(np.ma.getmaskarray)
