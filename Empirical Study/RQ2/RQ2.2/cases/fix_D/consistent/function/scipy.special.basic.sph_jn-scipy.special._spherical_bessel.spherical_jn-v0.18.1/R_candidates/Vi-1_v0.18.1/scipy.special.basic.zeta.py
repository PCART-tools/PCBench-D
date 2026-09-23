def zeta(x, q=None, out=None):
    r"""
    Riemann zeta function.

    The two-argument version is the Hurwitz zeta function:

    .. math:: \zeta(x, q) = \sum_{k=0}^{\infty} \frac{1}{(k + q)^x},

    Riemann zeta function corresponds to ``q = 1``.

    See also
    --------
    zetac

    """
    if q is None:
        q = 1
    return _zeta(x, q, out)
