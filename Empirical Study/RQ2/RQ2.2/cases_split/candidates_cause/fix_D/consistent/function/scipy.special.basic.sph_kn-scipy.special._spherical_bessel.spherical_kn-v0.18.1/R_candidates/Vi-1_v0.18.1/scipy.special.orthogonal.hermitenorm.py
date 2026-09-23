def hermitenorm(n, monic=False):
    """Return the nth order normalized Hermite polynomial, He_n(x), orthogonal
    over (-inf,inf) with weighting function exp(-(x/2)**2)
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w, mu0 = he_roots(n1, mu=True)
    wfunc = lambda x: exp(-x * x / 2.0)
    if n == 0:
        x, w = [], []
    hn = sqrt(2 * pi) * _gam(n + 1)
    kn = 1.0
    p = orthopoly1d(x, w, hn, kn, wfunc=wfunc, limits=(-inf, inf), monic=monic,
                    eval_func=lambda x: eval_hermitenorm(n, x))
    return p
