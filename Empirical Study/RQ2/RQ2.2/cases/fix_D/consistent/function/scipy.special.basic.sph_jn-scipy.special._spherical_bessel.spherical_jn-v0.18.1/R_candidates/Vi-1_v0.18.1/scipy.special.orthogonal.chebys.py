def chebys(n, monic=False):
    r"""Return nth order Chebyshev polynomial of second kind, :math:`S_n(x)`.
    Orthogonal over :math:`[-2, 2]` with weight function
    :math:`f(x) = \sqrt{1 - (x/2)^2}`.
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = s_roots(n1, mu=True)
    if n == 0:
        x, w = [], []
    hn = pi
    kn = 1.0
    p = orthopoly1d(x, w, hn, kn,
                    wfunc=lambda x: sqrt(1 - x * x / 4.0),
                    limits=(-2, 2), monic=monic)
    if not monic:
        factor = (n + 1.0) / p(2)
        p._scale(factor)
        p.__dict__['_eval_func'] = lambda x: eval_chebys(n, x)
    return p
