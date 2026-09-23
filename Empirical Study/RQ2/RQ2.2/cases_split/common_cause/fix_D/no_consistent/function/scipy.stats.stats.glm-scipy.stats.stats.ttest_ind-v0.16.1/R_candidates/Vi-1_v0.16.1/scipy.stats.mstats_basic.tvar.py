def tvar(a, limits=None, inclusive=(True,True)):
    a = a.astype(float).ravel()
    if limits is None:
        n = (~a.mask).sum()  # todo: better way to do that?
        r = trima(a, limits=limits, inclusive=inclusive).var() * (n/(n-1.))
    else:
        raise ValueError('mstats.tvar() with limits not implemented yet so far')

    return r
