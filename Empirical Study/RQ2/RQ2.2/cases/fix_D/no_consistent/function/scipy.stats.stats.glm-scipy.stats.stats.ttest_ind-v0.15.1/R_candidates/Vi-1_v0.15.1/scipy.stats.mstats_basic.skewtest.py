def skewtest(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    if axis is None:
        a = a.ravel()
        axis = 0
    b2 = skew(a,axis)
    n = a.count(axis)
    if np.min(n) < 8:
        raise ValueError(
            "skewtest is not valid with less than 8 samples; %i samples"
            " were given." % np.min(n))

    y = b2 * ma.sqrt(((n+1)*(n+3)) / (6.0*(n-2)))
    beta2 = (3.0*(n*n+27*n-70)*(n+1)*(n+3)) / ((n-2.0)*(n+5)*(n+7)*(n+9))
    W2 = -1 + ma.sqrt(2*(beta2-1))
    delta = 1/ma.sqrt(0.5*ma.log(W2))
    alpha = ma.sqrt(2.0/(W2-1))
    y = ma.where(y == 0, 1, y)
    Z = delta*ma.log(y/alpha + ma.sqrt((y/alpha)**2+1))
    return Z, 2 * distributions.norm.sf(np.abs(Z))
