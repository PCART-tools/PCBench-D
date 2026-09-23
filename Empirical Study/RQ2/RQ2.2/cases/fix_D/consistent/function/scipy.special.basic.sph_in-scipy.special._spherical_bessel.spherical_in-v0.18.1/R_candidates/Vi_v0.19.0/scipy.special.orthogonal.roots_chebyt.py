def roots_chebyt(n, mu=False):
    r"""Gauss-Chebyshev (first kind) quadrature.

    Computes the sample points and weights for Gauss-Chebyshev quadrature.
    The sample points are the roots of the n-th degree Chebyshev polynomial of
    the first kind, :math:`T_n(x)`.  These sample points and weights correctly
    integrate polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[-1, 1]` with weight function :math:`f(x) = 1/\sqrt{1 - x^2}`.

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
    numpy.polynomial.chebyshev.chebgauss
    """
    m = int(n)
    if n < 1 or n != m:
        raise ValueError('n must be a positive integer.')
    x = np.cos(np.arange(2 * m - 1, 0, -2) * pi / (2 * m))
    w = np.empty_like(x)
    w.fill(pi/m)
    if mu:
        return x, w, pi
    else:
        return x, w
