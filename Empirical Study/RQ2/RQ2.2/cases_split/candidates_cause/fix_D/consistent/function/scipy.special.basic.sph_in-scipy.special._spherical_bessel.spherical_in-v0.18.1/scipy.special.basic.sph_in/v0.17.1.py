def sph_in(n, z):
    """Compute spherical Bessel function in(z) and derivative.

    This function computes the value and first derivative of in(z) for all
    orders up to and including n.

    Parameters
    ----------
    n : int
        Maximum order of in to compute
    z : complex
        Argument at which to evaluate

    Returns
    -------
    in : ndarray
        Value of i0(z), ..., in(z)
    inp : ndarray
        First derivative i0'(z), ..., in'(z)

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 8.
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
        nm, In, Inp, kn, knp = specfun.csphik(n1, z)
    else:
        nm, In, Inp = specfun.sphi(n1, z)
    return In[:(n+1)], Inp[:(n+1)]
