def la_roots(n, alpha, mu=False):
    r"""Gauss-generalized Laguerre quadrature.

    Computes the sample points and weights for Gauss-generalized Laguerre
    quadrature. The sample points are the roots of the n-th degree generalized
    Laguerre polynomial, :math:`L^{\alpha}_n(x)`.  These sample points and
    weights correctly integrate polynomials of degree :math:`2n - 1` or less
    over the interval :math:`[0, \infty]` with weight function
    :math:`f(x) = x^{\alpha} e^{-x}`.

    Parameters
    ----------
    n : int
        quadrature order
    alpha : float
        alpha must be > -1
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
        raise ValueError("n must be a positive integer.")
    if alpha < -1:
        raise ValueError("alpha must be greater than -1.")

    mu0 = cephes.gamma(alpha + 1)

    if m == 1:
        x = np.array([alpha+1.0], 'd')
        w = np.array([mu0], 'd')
        if mu:
            return x, w, mu0
        else:
            return x, w

    an_func = lambda k: 2 * k + alpha + 1
    bn_func = lambda k: -np.sqrt(k * (k + alpha))
    f = lambda n, x: cephes.eval_genlaguerre(n, alpha, x)
    df = lambda n, x: (n*cephes.eval_genlaguerre(n, alpha, x)
                     - (n + alpha)*cephes.eval_genlaguerre(n-1, alpha, x))/x
    return _gen_roots_and_weights(m, mu0, an_func, bn_func, f, df, False, mu)
