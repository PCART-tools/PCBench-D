@np.deprecate(message="scipy.special.sph_jn is deprecated in scipy 0.18.0. "
                      "Use scipy.special.spherical_jn instead. "
                      "Note that the new function has a different signature.")
def sph_jn(n, z):
    """Compute spherical Bessel function jn(z) and derivative.

    This function computes the value and first derivative of jn(z) for all
    orders up to and including n.

    Parameters
    ----------
    n : int
        Maximum order of jn to compute
    z : complex
        Argument at which to evaluate

    Returns
    -------
    jn : ndarray
        Value of j0(z), ..., jn(z)
    jnp : ndarray
        First derivative j0'(z), ..., jn'(z)

    See also
    --------
    spherical_jn

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
        nm, jn, jnp, yn, ynp = specfun.csphjy(n1, z)
    else:
        nm, jn, jnp = specfun.sphj(n1, z)
    return jn[:(n+1)], jnp[:(n+1)]
