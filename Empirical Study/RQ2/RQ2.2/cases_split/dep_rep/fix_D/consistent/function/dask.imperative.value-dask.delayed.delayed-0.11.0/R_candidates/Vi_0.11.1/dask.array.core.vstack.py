@wraps(np.vstack)
def vstack(tup):
    tup = tuple(atleast_2d(x) for x in tup)
    return concatenate(tup, axis=0)
