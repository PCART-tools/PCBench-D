@wraps(np.ediff1d)
def ediff1d(ary, to_end=None, to_begin=None):
    ary = asarray(ary)

    aryf = ary.flatten()
    r = aryf[1:] - aryf[:-1]

    r = [r]
    if to_begin is not None:
        r = [asarray(to_begin).flatten()] + r
    if to_end is not None:
        r = r + [asarray(to_end).flatten()]
    r = concatenate(r)

    return r
