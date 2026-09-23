def riccati_yn(n, x):
    """Compute Ricatti-Bessel function of the second kind and its derivative.

    The Ricatti-Bessel function of the second kind is defined as :math:`x
    y_n(x)`, where :math:`y_n` is the spherical Bessel function of the second
    kind of order :math:`n`.

    This function computes the value and first derivative of the function for
    all orders up to and including `n`.

    Parameters
    ----------
    n : int
        Maximum order of function to compute
    x : float
        Argument at which to evaluate

    Returns
    -------
    yn : ndarray
        Value of y0(x), ..., yn(x)
    ynp : ndarray
        First derivative y0'(x), ..., yn'(x)

    Notes
    -----
    The computation is carried out via ascending recurrence, using the
    relation DLMF 10.51.1 [2]_.

    Wrapper for a Fortran routine created by Shanjie Zhang and Jianming
    Jin [1]_.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           http://jin.ece.illinois.edu/specfunc.html
    .. [2] NIST Digital Library of Mathematical Functions.
           http://dlmf.nist.gov/10.51.E1

    """
    if not (isscalar(n) and isscalar(x)):
        raise ValueError("arguments must be scalars.")
    if (n != floor(n)) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if (n == 0):
        n1 = 1
    else:
        n1 = n
    nm, jn, jnp = specfun.rcty(n1, x)
    return jn[:(n+1)], jnp[:(n+1)]
