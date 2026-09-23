def hermite(n, monic=False):
    r"""Physicist's Hermite polynomial.

    Defined by

    .. math::

        H_n(x) = (-1)^ne^{x^2}\frac{d^n}{dx^n}e^{-x^2};

    :math:`H_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    H : orthopoly1d
        Hermite polynomial.

    Notes
    -----
    The polynomials :math:`H_n` are orthogonal over :math:`(-\infty,
    \infty)` with weight function :math:`e^{-x^2}`.

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = roots_hermite(n1, mu=True)
    wfunc = lambda x: exp(-x * x)
    if n == 0:
        x, w = [], []
    hn = 2**n * _gam(n + 1) * sqrt(pi)
    kn = 2**n
    p = orthopoly1d(x, w, hn, kn, wfunc, (-inf, inf), monic,
                    lambda x: eval_hermite(n, x))
    return p
