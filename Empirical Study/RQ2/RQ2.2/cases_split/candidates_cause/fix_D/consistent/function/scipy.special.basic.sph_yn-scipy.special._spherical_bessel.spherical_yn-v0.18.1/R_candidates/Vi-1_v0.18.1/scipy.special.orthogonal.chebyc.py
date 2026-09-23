def chebyc(n, monic=False):
    """Return n-th order Chebyshev polynomial of first kind, :math:`C_n(x)`. 
    Orthogonal over :math:`[-2, 2]` with weight function
    :math:`f(x) = 1/\sqrt{1 - (x/2)^2}`
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = c_roots(n1, mu=True)
    if n == 0:
        x, w = [], []
    hn = 4 * pi * ((n == 0) + 1)
    kn = 1.0
    p = orthopoly1d(x, w, hn, kn,
                    wfunc=lambda x: 1.0 / sqrt(1 - x * x / 4.0),
                    limits=(-2, 2), monic=monic)
    if not monic:
        p._scale(2.0 / p(2))
        p.__dict__['_eval_func'] = lambda x: eval_chebyc(n, x)
    return p
