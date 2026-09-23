@np.deprecate(message="scipy.special.sph_kn is deprecated in scipy 0.18.0. "
                      "Use scipy.special.spherical_kn instead. "
                      "Note that the new function has a different signature.")
def sph_kn(n, z):
    """Compute spherical Bessel function kn(z) and derivative.

    This function computes the value and first derivative of kn(z) for all
    orders up to and including n.

    Parameters
    ----------
    n : int
        Maximum order of kn to compute
    z : complex
        Argument at which to evaluate

    Returns
    -------
    kn : ndarray
        Value of k0(z), ..., kn(z)
    knp : ndarray
        First derivative k0'(z), ..., kn'(z)

    See also
    --------
    spherical_kn

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
    if iscomplex(z) or less(z, 0):
        nm, In, Inp, kn, knp = specfun.csphik(n1, z)
    else:
        nm, kn, knp = specfun.sphk(n1, z)
    return kn[:(n+1)], knp[:(n+1)]
