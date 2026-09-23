def roots_sh_chebyu(n, mu=False):
    r"""Gauss-Chebyshev (second kind, shifted) quadrature.

    Computes the sample points and weights for Gauss-Chebyshev quadrature.
    The sample points are the roots of the n-th degree shifted Chebyshev
    polynomial of the second kind, :math:`U_n(x)`.  These sample points and
    weights correctly integrate polynomials of degree :math:`2n - 1` or less
    over the interval :math:`[0, 1]` with weight function
    :math:`f(x) = \sqrt{x - x^2}`.

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
    x = (x + 1) / 2
    m_us = cephes.beta(1.5, 1.5)
    w *= m_us / m
    if mu:
        return x, w, m_us
    else:
        return x, w
