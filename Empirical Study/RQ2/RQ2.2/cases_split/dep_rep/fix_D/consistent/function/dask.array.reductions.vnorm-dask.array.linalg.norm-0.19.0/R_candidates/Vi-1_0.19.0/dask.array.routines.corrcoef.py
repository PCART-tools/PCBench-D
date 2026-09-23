@wraps(np.corrcoef)
def corrcoef(x, y=None, rowvar=1):

    from .ufunc import sqrt
    from .creation import diag

    c = cov(x, y, rowvar)
    if c.shape == ():
        return c / c
    d = diag(c)
    d = d.reshape((d.shape[0], 1))
    sqr_d = sqrt(d)
    return (c / sqr_d) / sqr_d.T
