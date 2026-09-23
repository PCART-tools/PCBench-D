def sh_chebyu(n, monic=False):
    r"""Shifted Chebyshev polynomial of the second kind.

    Defined as :math:`U^*_n(x) = U_n(2x - 1)` for :math:`U_n` the nth
    Chebyshev polynomial of the second kind.

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
        Shifted Chebyshev polynomial of the second kind.

    Notes
    -----
    The polynomials :math:`U^*_n` are orthogonal over :math:`[0, 1]`
    with weight function :math:`(x - x^2)^{1/2}`.

    """
    base = sh_jacobi(n, 2.0, 1.5, monic=monic)
    if monic:
        return base
    factor = 4**n
    base._scale(factor)
    return base
