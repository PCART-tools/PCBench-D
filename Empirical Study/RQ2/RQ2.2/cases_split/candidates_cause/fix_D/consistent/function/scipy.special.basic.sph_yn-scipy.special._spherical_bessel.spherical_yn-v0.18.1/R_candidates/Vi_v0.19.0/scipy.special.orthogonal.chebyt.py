def chebyt(n, monic=False):
    r"""Chebyshev polynomial of the first kind.

    Defined to be the solution of

    .. math::
        (1 - x^2)\frac{d^2}{dx^2}T_n - x\frac{d}{dx}T_n + n^2T_n = 0;

    :math:`T_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    T : orthopoly1d
        Chebyshev polynomial of the first kind.

    Notes
    -----
    The polynomials :math:`T_n` are orthogonal over :math:`[-1, 1]`
    with weight function :math:`(1 - x^2)^{-1/2}`.

    See Also
    --------
    chebyu : Chebyshev polynomial of the second kind.

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    wfunc = lambda x: 1.0 / sqrt(1 - x * x)
    if n == 0:
        return orthopoly1d([], [], pi, 1.0, wfunc, (-1, 1), monic,
                           lambda x: eval_chebyt(n, x))
    n1 = n
    x, w, mu = roots_chebyt(n1, mu=True)
    hn = pi / 2
    kn = 2**(n - 1)
    p = orthopoly1d(x, w, hn, kn, wfunc, (-1, 1), monic,
                    lambda x: eval_chebyt(n, x))
    return p
