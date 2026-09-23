def laguerre(n, monic=False):
    r"""Laguerre polynomial.

    Defined to be the solution of

    .. math::
        x\frac{d^2}{dx^2}L_n + (1 - x)\frac{d}{dx}L_n + nL_n = 0;

    :math:`L_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    L : orthopoly1d
        Laguerre Polynomial.

    Notes
    -----
    The polynomials :math:`L_n` are orthogonal over :math:`[0,
    \infty)` with weight function :math:`e^{-x}`.

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = roots_laguerre(n1, mu=True)
    if n == 0:
        x, w = [], []
    hn = 1.0
    kn = (-1)**n / _gam(n + 1)
    p = orthopoly1d(x, w, hn, kn, lambda x: exp(-x), (0, inf), monic,
                    lambda x: eval_laguerre(n, x))
    return p
