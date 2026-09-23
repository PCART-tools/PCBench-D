def sh_jacobi(n, p, q, monic=False):
    """Returns the nth order Jacobi polynomial, G_n(p,q,x)
    orthogonal over [0,1] with weighting function
    (1-x)**(p-q) (x)**(q-1) with p>q-1 and q > 0.
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    wfunc = lambda x: (1.0 - x)**(p - q) * (x)**(q - 1.)
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (-1, 1), monic,
                           eval_func=np.ones_like)
    n1 = n
    x, w, mu0 = js_roots(n1, p, q, mu=True)
    hn = _gam(n + 1) * _gam(n + q) * _gam(n + p) * _gam(n + p - q + 1)
    hn /= (2 * n + p) * (_gam(2 * n + p)**2)
    # kn = 1.0 in standard form so monic is redundant.  Kept for compatibility.
    kn = 1.0
    pp = orthopoly1d(x, w, hn, kn, wfunc=wfunc, limits=(0, 1), monic=monic,
                     eval_func=lambda x: eval_sh_jacobi(n, p, q, x))
    return pp
