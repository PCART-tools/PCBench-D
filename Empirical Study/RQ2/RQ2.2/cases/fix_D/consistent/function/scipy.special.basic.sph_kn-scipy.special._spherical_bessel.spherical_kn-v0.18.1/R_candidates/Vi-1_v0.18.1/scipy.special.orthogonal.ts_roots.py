def ts_roots(n, mu=False):
    r"""Gauss-Chebyshev (first kind, shifted) quadrature.

    Computes the sample points and weights for Gauss-Chebyshev quadrature.
    The sample points are the roots of the n-th degree shifted Chebyshev
    polynomial of the first kind, :math:`T_n(x)`.  These sample points and
    weights correctly integrate polynomials of degree :math:`2n - 1` or less
    over the interval :math:`[0, 1]` with weight function
    :math:`f(x) = 1/\sqrt{x - x^2}`.

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
    xw = t_roots(n, mu)
    return ((xw[0] + 1) / 2,) + xw[1:]
