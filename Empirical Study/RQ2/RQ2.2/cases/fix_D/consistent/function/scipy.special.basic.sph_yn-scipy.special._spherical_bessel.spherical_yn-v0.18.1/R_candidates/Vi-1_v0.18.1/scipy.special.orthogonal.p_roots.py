def p_roots(n, mu=False):
    r"""Gauss-Legendre quadrature.

    Computes the sample points and weights for Gauss-Legendre quadrature.
    The sample points are the roots of the n-th degree Legendre polynomial
    :math:`P_n(x)`.  These sample points and weights correctly integrate
    polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[-1, 1]` with weight function :math:`f(x) = 1.0`.

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
    numpy.polynomial.legendre.leggauss
    """
    m = int(n)
    if n < 1 or n != m:
        raise ValueError("n must be a positive integer.")

    mu0 = 2.0
    an_func = lambda k: 0.0 * k
    bn_func = lambda k: k * np.sqrt(1.0 / (4 * k * k - 1))
    f = cephes.eval_legendre
    df = lambda n, x: (-n*x*cephes.eval_legendre(n, x)
                     + n*cephes.eval_legendre(n-1, x))/(1-x**2)
    return _gen_roots_and_weights(m, mu0, an_func, bn_func, f, df, True, mu)
