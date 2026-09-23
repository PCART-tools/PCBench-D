def lqn(n, z):
    """Legendre functions of the second kind, Qn(z).

    Compute sequence of Legendre functions of the second kind, Qn(z) and
    derivatives for all degrees from 0 to n (inclusive).

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError("arguments must be scalars.")
    if (n != floor(n)) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if (n < 1):
        n1 = 1
    else:
        n1 = n
    if iscomplex(z):
        qn, qd = specfun.clqn(n1, z)
    else:
        qn, qd = specfun.lqnb(n1, z)
    return qn[:(n+1)], qd[:(n+1)]
