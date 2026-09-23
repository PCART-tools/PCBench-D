def ivp(v, z, n=1):
    """Compute nth derivative of modified Bessel function Iv(z) with respect
    to `z`.

    Parameters
    ----------
    v : array_like of float
        Order of Bessel function
    z : array_like of complex
        Argument at which to evaluate the derivative
    n : int, default 1
        Order of derivative

    Notes
    -----
    The derivative is computed using the relation DLFM 10.29.5 [2]_.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 6.
           http://jin.ece.illinois.edu/specfunc.html
    .. [2] NIST Digital Library of Mathematical Functions.
           http://dlmf.nist.gov/10.29.E5

    """
    if not isinstance(n, int) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if n == 0:
        return iv(v, z)
    else:
        return _bessel_diff_formula(v, z, n, iv, 1)
