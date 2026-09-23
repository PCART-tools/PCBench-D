def jacobi(n, alpha, beta, monic=False):
    r"""Jacobi polynomial.

    Defined to be the solution of

    .. math::
        (1 - x^2)\frac{d^2}{dx^2}P_n^{(\alpha, \beta)}
          + (\beta - \alpha - (\alpha + \beta + 2)x)
            \frac{d}{dx}P_n^{(\alpha, \beta)}
          + n(n + \alpha + \beta + 1)P_n^{(\alpha, \beta)} = 0

    for :math:`\alpha, \beta > -1`; :math:`P_n^{(\alpha, \beta)}` is a
    polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    alpha : float
        Parameter, must be greater than -1.
    beta : float
        Parameter, must be greater than -1.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    P : orthopoly1d
        Jacobi polynomial.

    Notes
    -----
    For fixed :math:`\alpha, \beta`, the polynomials
    :math:`P_n^{(\alpha, \beta)}` are orthogonal over :math:`[-1, 1]`
    with weight function :math:`(1 - x)^\alpha(1 + x)^\beta`.

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    wfunc = lambda x: (1 - x)**alpha * (1 + x)**beta
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (-1, 1), monic,
                           eval_func=np.ones_like)
    x, w, mu = roots_jacobi(n, alpha, beta, mu=True)
    ab1 = alpha + beta + 1.0
    hn = 2**ab1 / (2 * n + ab1) * _gam(n + alpha + 1)
    hn *= _gam(n + beta + 1.0) / _gam(n + 1) / _gam(n + ab1)
    kn = _gam(2 * n + ab1) / 2.0**n / _gam(n + 1) / _gam(n + ab1)
    # here kn = coefficient on x^n term
    p = orthopoly1d(x, w, hn, kn, wfunc, (-1, 1), monic,
                    lambda x: eval_jacobi(n, alpha, beta, x))
    return p
