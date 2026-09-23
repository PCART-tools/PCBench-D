def obrientransform(*args):
    """
Computes a transform on input data (any number of columns).  Used to
test for homogeneity of variance prior to running one-way stats.  Each
array in *args is one level of a factor.  If an F_oneway() run on the
transformed data and found significant, variances are unequal.   From
Maxwell and Delaney, p.112.

Returns: transformed data for use in an ANOVA
    """
    data = argstoarray(*args).T
    v = data.var(axis=0,ddof=1)
    m = data.mean(0)
    n = data.count(0).astype(float)
    # result = ((N-1.5)*N*(a-m)**2 - 0.5*v*(n-1))/((n-1)*(n-2))
    data -= m
    data **= 2
    data *= (n-1.5)*n
    data -= 0.5*v*(n-1)
    data /= (n-1.)*(n-2.)
    if not ma.allclose(v,data.mean(0)):
        raise ValueError("Lack of convergence in obrientransform.")
    return data
