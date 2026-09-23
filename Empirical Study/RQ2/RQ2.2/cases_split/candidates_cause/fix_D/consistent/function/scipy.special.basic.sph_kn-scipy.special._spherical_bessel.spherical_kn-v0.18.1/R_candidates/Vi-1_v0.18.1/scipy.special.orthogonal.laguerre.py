def laguerre(n, monic=False):
    """Return the nth order Laguerre polynoimal, L_n(x), orthogonal over
    [0,inf) with weighting function exp(-x)
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = l_roots(n1, mu=True)
    if n == 0:
        x, w = [], []
    hn = 1.0
    kn = (-1)**n / _gam(n + 1)
    p = orthopoly1d(x, w, hn, kn, lambda x: exp(-x), (0, inf), monic,
                    lambda x: eval_laguerre(n, x))
    return p
