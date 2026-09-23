def pointbiserialr(x, y):
    x = ma.fix_invalid(x, copy=True).astype(bool)
    y = ma.fix_invalid(y, copy=True).astype(float)
    # Get rid of the missing data
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    if m is not nomask:
        unmask = np.logical_not(m)
        x = x[unmask]
        y = y[unmask]

    n = len(x)
    # phat is the fraction of x values that are True
    phat = x.sum() / float(n)
    y0 = y[~x]  # y-values where x is False
    y1 = y[x]  # y-values where x is True
    y0m = y0.mean()
    y1m = y1.mean()

    rpb = (y1m - y0m)*np.sqrt(phat * (1-phat)) / y.std()

    df = n-2
    t = rpb*ma.sqrt(df/(1.0-rpb**2))
    prob = betai(0.5*df, 0.5, df/(df+t*t))

    PointbiserialrResult = namedtuple('PointbiserialrResult', ('correlation',
                                                               'pvalue'))
    return PointbiserialrResult(rpb, prob)
