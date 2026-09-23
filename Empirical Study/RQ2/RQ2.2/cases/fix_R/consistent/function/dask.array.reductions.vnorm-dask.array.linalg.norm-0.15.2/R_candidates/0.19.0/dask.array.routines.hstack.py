@wraps(np.hstack)
def hstack(tup):
    if all(x.ndim == 1 for x in tup):
        return concatenate(tup, axis=0)
    else:
        return concatenate(tup, axis=1)
