def roots_jacobi(n, alpha, beta, mu=False):
    r"""Gauss-Jacobi quadrature.

    Computes the sample points and weights for Gauss-Jacobi quadrature. The
    sample points are the roots of the n-th degree Jacobi polynomial,
    :math:`P^{\alpha, \beta}_n(x)`.  These sample points and weights
    correctly integrate polynomials of degree :math:`2n - 1` or less over the
    interval :math:`[-1, 1]` with weight function
    :math:`f(x) = (1 - x)^{\alpha} (1 + x)^{\beta}`.

    Parameters
    ----------
    n : int
        quadrature order
    alpha : float
        alpha must be > -1
    beta : float
        beta must be > 0
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
    if alpha <= -1 or beta <= -1:
        raise ValueError("alpha and beta must be greater than -1.")

    if alpha == 0.0 and beta == 0.0:
        return roots_legendre(m, mu)
    if alpha == beta:
        return roots_gegenbauer(m, alpha+0.5, mu)

    mu0 = 2.0**(alpha+beta+1)*cephes.beta(alpha+1, beta+1)
    a = alpha
    b = beta
    if a + b == 0.0:
        an_func = lambda k: np.where(k == 0, (b-a)/(2+a+b), 0.0)
    else:
        an_func = lambda k: np.where(k == 0, (b-a)/(2+a+b),
                  (b*b - a*a) / ((2.0*k+a+b)*(2.0*k+a+b+2)))

    bn_func = lambda k: 2.0 / (2.0*k+a+b)*np.sqrt((k+a)*(k+b) / (2*k+a+b+1)) \
              * np.where(k == 1, 1.0, np.sqrt(k*(k+a+b) / (2.0*k+a+b-1)))

    f = lambda n, x: cephes.eval_jacobi(n, a, b, x)
    df = lambda n, x: 0.5 * (n + a + b + 1) \
                      * cephes.eval_jacobi(n-1, a+1, b+1, x)
    return _gen_roots_and_weights(m, mu0, an_func, bn_func, f, df, False, mu)
