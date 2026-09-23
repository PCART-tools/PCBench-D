def fresnel_zeros(nt):
    """Compute nt complex zeros of sine and cosine Fresnel integrals S(z) and C(z).

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if (floor(nt) != nt) or (nt <= 0) or not isscalar(nt):
        raise ValueError("Argument must be positive scalar integer.")
    return specfun.fcszo(2, nt), specfun.fcszo(1, nt)
