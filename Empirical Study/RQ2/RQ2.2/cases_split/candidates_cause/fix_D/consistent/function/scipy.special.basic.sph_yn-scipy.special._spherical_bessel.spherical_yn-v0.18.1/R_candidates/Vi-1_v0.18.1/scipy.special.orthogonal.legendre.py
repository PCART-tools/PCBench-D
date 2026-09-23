def legendre(n, monic=False):
    """
    Legendre polynomial coefficients

    Returns the nth-order Legendre polynomial, P_n(x), orthogonal over
    [-1, 1] with weight function 1.

    Parameters
    ----------
    n
        Order of the polynomial
    monic : bool, optional
        If True, output is a monic polynomial (normalized so the leading
        coefficient is 1).  Default is False.

    Returns
    -------
    P : orthopoly1d
        The Legendre polynomial object

    Examples
    --------
    Generate the 3rd-order Legendre polynomial 1/2*(5x^3 + 0x^2 - 3x + 0):

    >>> from scipy.special import legendre
    >>> legendre(3)
    poly1d([ 2.5,  0. , -1.5,  0. ])

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = p_roots(n1, mu=True)
    if n == 0:
        x, w = [], []
    hn = 2.0 / (2 * n + 1)
    kn = _gam(2 * n + 1) / _gam(n + 1)**2 / 2.0**n
    p = orthopoly1d(x, w, hn, kn, wfunc=lambda x: 1.0, limits=(-1, 1),
                    monic=monic, eval_func=lambda x: eval_legendre(n, x))
    return p
