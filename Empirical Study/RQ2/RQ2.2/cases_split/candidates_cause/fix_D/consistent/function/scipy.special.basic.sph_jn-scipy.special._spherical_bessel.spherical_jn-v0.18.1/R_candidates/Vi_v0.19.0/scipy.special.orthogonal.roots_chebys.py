def roots_chebys(n, mu=False):
    r"""Gauss-Chebyshev (second kind) quadrature.

    Computes the sample points and weights for Gauss-Chebyshev quadrature.
    The sample points are the roots of the n-th degree Chebyshev polynomial of
    the second kind, :math:`S_n(x)`.  These sample points and weights correctly
    integrate polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[-2, 2]` with weight function :math:`f(x) = \sqrt{1 - (x/2)^2}`.

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
    x, w, m = roots_chebyu(n, True)
    x *= 2
    w *= 2
    m *= 2
    if mu:
        return x, w, m
    else:
        return x, w
