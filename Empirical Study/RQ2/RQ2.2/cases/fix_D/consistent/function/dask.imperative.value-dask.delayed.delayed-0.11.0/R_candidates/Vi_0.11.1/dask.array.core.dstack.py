@wraps(np.dstack)
def dstack(tup):
    tup = tuple(atleast_3d(x) for x in tup)
    return concatenate(tup, axis=2)
