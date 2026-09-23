def u_roots(n, mu=False):
    r"""Gauss-Chebyshev (second kind) quadrature.

    Computes the sample points and weights for Gauss-Chebyshev quadrature.
    The sample points are the roots of the n-th degree Chebyshev polynomial of
    the second kind, :math:`U_n(x)`.  These sample points and weights correctly
    integrate polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[-1, 1]` with weight function :math:`f(x) = \sqrt{1 - x^2}`.

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
    m = int(n)
    if n < 1 or n != m:
        raise ValueError('n must be a positive integer.')
    t = np.arange(m, 0, -1) * pi / (m + 1)
    x = np.cos(t)
    w = pi * np.sin(t)**2 / (m + 1)
    if mu:
        return x, w, pi / 2
    else:
        return x, w
