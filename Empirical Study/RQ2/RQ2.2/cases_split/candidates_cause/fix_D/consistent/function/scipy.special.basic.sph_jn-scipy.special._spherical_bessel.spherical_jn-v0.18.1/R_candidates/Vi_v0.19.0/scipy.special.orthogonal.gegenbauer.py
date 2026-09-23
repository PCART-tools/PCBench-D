def gegenbauer(n, alpha, monic=False):
    r"""Gegenbauer (ultraspherical) polynomial.

    Defined to be the solution of

    .. math::
        (1 - x^2)\frac{d^2}{dx^2}C_n^{(\alpha)}
          - (2\alpha + 1)x\frac{d}{dx}C_n^{(\alpha)}
          + n(n + 2\alpha)C_n^{(\alpha)} = 0

    for :math:`\alpha > -1/2`; :math:`C_n^{(\alpha)}` is a polynomial
    of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    C : orthopoly1d
        Gegenbauer polynomial.

    Notes
    -----
    The polynomials :math:`C_n^{(\alpha)}` are orthogonal over
    :math:`[-1,1]` with weight function :math:`(1 - x^2)^{(\alpha -
    1/2)}`.

    """
    base = jacobi(n, alpha - 0.5, alpha - 0.5, monic=monic)
    if monic:
        return base
    #  Abrahmowitz and Stegan 22.5.20
    factor = (_gam(2*alpha + n) * _gam(alpha + 0.5) /
              _gam(2*alpha) / _gam(alpha + 0.5 + n))
    base._scale(factor)
    base.__dict__['_eval_func'] = lambda x: eval_gegenbauer(float(n), alpha, x)
    return base
