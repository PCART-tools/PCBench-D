def roots_laguerre(n, mu=False):
    r"""Gauss-Laguerre quadrature.

    Computes the sample points and weights for Gauss-Laguerre quadrature.
    The sample points are the roots of the n-th degree Laguerre polynomial,
    :math:`L_n(x)`.  These sample points and weights correctly integrate
    polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[0, \infty]` with weight function :math:`f(x) = e^{-x}`.

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
    numpy.polynomial.laguerre.laggauss
    """
    return roots_genlaguerre(n, 0.0, mu=mu)
