def chebyu(n, monic=False):
    r"""Chebyshev polynomial of the second kind.

    Defined to be the solution of

    .. math::
        (1 - x^2)\frac{d^2}{dx^2}U_n - 3x\frac{d}{dx}U_n
          + n(n + 2)U_n = 0;

    :math:`U_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    U : orthopoly1d
        Chebyshev polynomial of the second kind.

    Notes
    -----
    The polynomials :math:`U_n` are orthogonal over :math:`[-1, 1]`
    with weight function :math:`(1 - x^2)^{1/2}`.

    See Also
    --------
    chebyt : Chebyshev polynomial of the first kind.

    """
    base = jacobi(n, 0.5, 0.5, monic=monic)
    if monic:
        return base
    factor = sqrt(pi) / 2.0 * _gam(n + 2) / _gam(n + 1.5)
    base._scale(factor)
    return base
