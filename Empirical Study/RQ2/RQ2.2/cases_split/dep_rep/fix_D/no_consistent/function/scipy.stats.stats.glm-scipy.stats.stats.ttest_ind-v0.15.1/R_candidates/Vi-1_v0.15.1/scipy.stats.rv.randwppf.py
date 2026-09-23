@deprecate(message="Deprecated in scipy 0.14.0, use "
                   "distribution-specific rvs() method instead")
def randwppf(ppf, args=(), size=None):
    """
    returns an array of randomly distributed integers of a distribution
    whose percent point function (inverse of the CDF or quantile function)
    is given.

    args is a tuple of extra arguments to the ppf function (i.e. shape,
    location, scale), and size is the size of the output.  Note the ppf
    function must accept an array of q values to compute over.

    """
    U = random_sample(size=size)
    return ppf(*(U,)+args)
