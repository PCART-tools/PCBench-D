def linregress(*args):
    if len(args) == 1:  # more than 1D array?
        args = ma.array(args[0], copy=True)
        if len(args) == 2:
            x = args[0]
            y = args[1]
        else:
            x = args[:,0]
            y = args[:,1]
    else:
        x = ma.array(args[0]).flatten()
        y = ma.array(args[1]).flatten()
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    if m is not nomask:
        x = ma.array(x,mask=m)
        y = ma.array(y,mask=m)
    n = len(x)
    (xmean, ymean) = (x.mean(), y.mean())
    (xm, ym) = (x-xmean, y-ymean)
    (Sxx, Syy) = (ma.add.reduce(xm*xm), ma.add.reduce(ym*ym))
    Sxy = ma.add.reduce(xm*ym)
    r_den = ma.sqrt(Sxx*Syy)
    if r_den == 0.0:
        r = 0.0
    else:
        r = Sxy / r_den
        if (r > 1.0):
            r = 1.0  # from numerical error
    # z = 0.5*log((1.0+r+TINY)/(1.0-r+TINY))
    df = n-2
    t = r * ma.sqrt(df/(1.0-r*r))
    prob = betai(0.5*df,0.5,df/(df+t*t))
    slope = Sxy / Sxx
    intercept = ymean - slope*xmean
    sterrest = ma.sqrt(1.-r*r) * y.std()
    return slope, intercept, r, prob, sterrest
