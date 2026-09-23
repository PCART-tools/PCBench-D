@wraps(np.flatnonzero)
def flatnonzero(a):
    return argwhere(asarray(a).ravel())[:, 0]
