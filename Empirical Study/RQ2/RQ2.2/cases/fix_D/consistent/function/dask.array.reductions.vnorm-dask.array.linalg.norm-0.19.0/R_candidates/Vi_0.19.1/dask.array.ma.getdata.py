@wraps(np.ma.getdata)
def getdata(a):
    a = asanyarray(a)
    return a.map_blocks(np.ma.getdata)
