def hermite(n, monic=False):
    """Return the nth order Hermite polynomial, H_n(x), orthogonal over
    (-inf,inf) with weighting function exp(-x**2)
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = h_roots(n1, mu=True)
    wfunc = lambda x: exp(-x * x)
    if n == 0:
        x, w = [], []
    hn = 2**n * _gam(n + 1) * sqrt(pi)
    kn = 2**n
    p = orthopoly1d(x, w, hn, kn, wfunc, (-inf, inf), monic,
                    lambda x: eval_hermite(n, x))
    return p
