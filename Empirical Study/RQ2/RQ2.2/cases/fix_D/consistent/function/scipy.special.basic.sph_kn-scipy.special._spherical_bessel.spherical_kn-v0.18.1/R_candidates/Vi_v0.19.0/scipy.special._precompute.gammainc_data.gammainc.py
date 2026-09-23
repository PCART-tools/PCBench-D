def gammainc(a, x, dps=50, maxterms=10**8):
    """Compute gammainc exactly like mpmath does but allow for more
    summands in hypercomb. See

    mpmath/functions/expintegrals.py#L134
    
    in the mpmath github repository.

    """
    with mp.workdps(dps):
        z, a, b = mp.mpf(a), mp.mpf(x), mp.mpf(x)
        G = [z]
        negb = mp.fneg(b, exact=True)

        def h(z):
            T1 = [mp.exp(negb), b, z], [1, z, -1], [], G, [1], [1+z], b
            return (T1,)

        res = mp.hypercomb(h, [z], maxterms=maxterms)
        return mpf2float(res)
