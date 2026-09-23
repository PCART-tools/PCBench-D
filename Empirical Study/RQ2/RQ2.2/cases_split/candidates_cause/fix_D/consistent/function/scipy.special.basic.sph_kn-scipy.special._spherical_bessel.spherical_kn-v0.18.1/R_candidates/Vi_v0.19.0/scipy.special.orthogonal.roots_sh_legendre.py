def roots_sh_legendre(n, mu=False):
    r"""Gauss-Legendre (shifted) quadrature.

    Computes the sample points and weights for Gauss-Legendre quadrature.
    The sample points are the roots of the n-th degree shifted Legendre
    polynomial :math:`P^*_n(x)`.  These sample points and weights correctly
    integrate polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[0, 1]` with weight function :math:`f(x) = 1.0`.

    Parameters
    ----------
    n : int
        quadrature order
    mu : bool, optional
        If True, return the sum of the weights, optional.

    Returns
    -------
    x : ndarray
        Sample points
    w : ndarray
        Weights
    mu : float
        Sum of the weights

    See Also
    --------
    scipy.integrate.quadrature
    scipy.integrate.fixed_quad
    """
    x, w = roots_legendre(n)
    x = (x + 1) / 2
    w /= 2
    if mu:
        return x, w, 1.0
    else:
        return x, w
