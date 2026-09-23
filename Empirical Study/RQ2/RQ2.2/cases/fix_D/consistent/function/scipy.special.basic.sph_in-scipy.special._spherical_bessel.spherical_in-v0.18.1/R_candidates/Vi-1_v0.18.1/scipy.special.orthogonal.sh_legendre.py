def sh_legendre(n, monic=False):
    """Returns the nth order shifted Legendre polynomial, P^*_n(x), orthogonal
    over [0,1] with weighting function 1.
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    wfunc = lambda x: 0.0 * x + 1.0
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (0, 1), monic,
                           lambda x: eval_sh_legendre(n, x))
    x, w, mu0 = ps_roots(n, mu=True)
    hn = 1.0 / (2 * n + 1.0)
    kn = _gam(2 * n + 1) / _gam(n + 1)**2
    p = orthopoly1d(x, w, hn, kn, wfunc, limits=(0, 1), monic=monic,
                    eval_func=lambda x: eval_sh_legendre(n, x))
    return p
