def genlaguerre(n, alpha, monic=False):
    r"""Generalized (associated) Laguerre polynomial.

    Defined to be the solution of

    .. math::
        x\frac{d^2}{dx^2}L_n^{(\alpha)} 
          + (\alpha + 1 - x)\frac{d}{dx}L_n^{(\alpha)}
          + nL_n^{(\alpha)} = 0,

    where :math:`\alpha > -1`; :math:`L_n^{(\alpha)}` is a polynomial
    of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    alpha : float
        Parameter, must be greater than -1.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    L : orthopoly1d
        Generalized Laguerre polynomial.

    Notes
    -----
    For fixed :math:`\alpha`, the polynomials :math:`L_n^{(\alpha)}`
    are orthogonal over :math:`[0, \infty)` with weight function
    :math:`e^{-x}x^\alpha`.

    The Laguerre polynomials are the special case where :math:`\alpha
    = 0`.

    See Also
    --------
    laguerre : Laguerre polynomial.

    """
    if alpha <= -1:
        raise ValueError("alpha must be > -1")
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = roots_genlaguerre(n1, alpha, mu=True)
    wfunc = lambda x: exp(-x) * x**alpha
    if n == 0:
        x, w = [], []
    hn = _gam(n + alpha + 1) / _gam(n + 1)
    kn = (-1)**n / _gam(n + 1)
    p = orthopoly1d(x, w, hn, kn, wfunc, (0, inf), monic,
                    lambda x: eval_genlaguerre(n, alpha, x))
    return p
