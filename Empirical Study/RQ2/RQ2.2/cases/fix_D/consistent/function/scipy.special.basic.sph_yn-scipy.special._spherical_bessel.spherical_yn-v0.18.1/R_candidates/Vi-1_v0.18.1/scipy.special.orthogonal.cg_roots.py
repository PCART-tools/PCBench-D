def cg_roots(n, alpha, mu=False):
    r"""Gauss-Gegenbauer quadrature.

    Computes the sample points and weights for Gauss-Gegenbauer quadrature.
    The sample points are the roots of the n-th degree Gegenbauer polynomial,
    :math:`C^{\alpha}_n(x)`.  These sample points and weights correctly
    integrate polynomials of degree :math:`2n - 1` or less over the interval
    :math:`[-1, 1]` with weight function
    :math:`f(x) = (1 - x^2)^{\alpha - 1/2}`.

    Parameters
    ----------
    n : int
        quadrature order
    alpha : float
        alpha must be > -0.5
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
    if alpha < -0.5:
        raise ValueError("alpha must be greater than -0.5.")
    elif alpha == 0.0:
        # C(n,0,x) == 0 uniformly, however, as alpha->0, C(n,alpha,x)->T(n,x)
        # strictly, we should just error out here, since the roots are not
        # really defined, but we used to return something useful, so let's
        # keep doing so.
        return t_roots(n, mu)

    mu0 = np.sqrt(np.pi) * cephes.gamma(alpha + 0.5) / cephes.gamma(alpha + 1)
    an_func = lambda k: 0.0 * k
    bn_func = lambda k: np.sqrt(k * (k + 2 * alpha - 1)
                        / (4 * (k + alpha) * (k + alpha - 1)))
    f = lambda n, x: cephes.eval_gegenbauer(n, alpha, x)
    df = lambda n, x: (-n*x*cephes.eval_gegenbauer(n, alpha, x)
         + (n + 2*alpha - 1)*cephes.eval_gegenbauer(n-1, alpha, x))/(1-x**2)
    return _gen_roots_and_weights(m, mu0, an_func, bn_func, f, df, True, mu)
