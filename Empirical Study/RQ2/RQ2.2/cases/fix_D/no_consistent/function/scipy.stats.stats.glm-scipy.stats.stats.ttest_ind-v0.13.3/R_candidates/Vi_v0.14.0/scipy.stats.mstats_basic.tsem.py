def tsem(a, limits=None, inclusive=(True,True)):
    a = ma.asarray(a).ravel()
    if limits is None:
        n = float(a.count())
        return a.std()/ma.sqrt(n)
    am = trima(a.ravel(), limits, inclusive)
    sd = np.sqrt(am.var())
    return sd / am.count()
