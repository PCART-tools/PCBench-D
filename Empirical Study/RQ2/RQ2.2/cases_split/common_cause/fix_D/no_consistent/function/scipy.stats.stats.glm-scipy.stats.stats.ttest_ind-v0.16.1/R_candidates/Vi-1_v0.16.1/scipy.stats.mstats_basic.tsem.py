def tsem(a, limits=None, inclusive=(True,True)):
    a = ma.asarray(a).ravel()
    if limits is None:
        n = float(a.count())
        return a.std(ddof=1)/ma.sqrt(n)

    am = trima(a.ravel(), limits, inclusive)
    sd = np.sqrt(am.var(ddof=1))
    return sd / np.sqrt(am.count())
