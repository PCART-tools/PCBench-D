def kelvin_zeros(nt):
    """Compute nt zeros of all Kelvin functions.

    Returned in a length-8 tuple of arrays of length nt.  The tuple contains
    the arrays of zeros of (ber, bei, ker, kei, ber', bei', ker', kei').

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("nt must be positive integer scalar.")
    return (specfun.klvnzo(nt, 1),
            specfun.klvnzo(nt, 2),
            specfun.klvnzo(nt, 3),
            specfun.klvnzo(nt, 4),
            specfun.klvnzo(nt, 5),
            specfun.klvnzo(nt, 6),
            specfun.klvnzo(nt, 7),
            specfun.klvnzo(nt, 8))
